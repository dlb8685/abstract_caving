from django.shortcuts import render
from game import models, utils, fncache, redis_info
from django.middleware.csrf import get_token
from json import loads
from django.conf import settings
import redis


# Create your views here.
def game_home(request):
    '''
    If the method is GET, it means that someone is just landing
        ID = 1, show the room that explains what is going on
        Some sample text is shown
        -- How to click on other links, etc.
        -- Return to: Usually you will be able to return to a previous room. 
            Since this room is the starting point of the game, it is the lone exception.
        -- Usually you will have additional rooms to venture into. 
            If not, it means you have reached a dead-end.
        -- Some rooms contain a point total. 
            Try to get the maximum score you can with 20 moves, 100 moves, 500 moves, 1,000 moves, 
                or as many as you have time for.
        -- This map never changes. There are almost 10,000 rooms. 
            You can start over and play as many games as you want to maximize your score, 
            or to simply learn new things.
    If the method is POST, it means that someone is in the midst of a game
        -- Score under the game window should be updated
        -- Will only post titles, not ids, so user can't snoop around page source
        -- Parameters will be: 
            current_cavern, from_cavern, running move_count, running points, 
            and visited_room_ids, 
                set of ids where points have been accumulated to avoid double-counting 
    '''

    if request.method == 'GET':
        csrf_token = get_token(request)
        context_dictionary = game_home_get()
        return render(request, 'game/home.html', context_dictionary)
        
    if request.method == 'POST':
        # raw text values
        move_count = request.POST.get('move_count')
        total_points = request.POST.get('total_points')
        visited_room_ids = request.POST.get('visited_room_ids')
        from_title = request.POST.get('from_title')
        current_title = request.POST.get('current_title')
        # convert to usable
        move_count = int(move_count)
        total_points = int(total_points)
        if visited_room_ids == '0':
            visited_room_ids = []
        else:
            visited_room_ids = loads(visited_room_ids)
        context_dictionary = cavern_title_get_to_caverns(from_title, current_title)
        if context_dictionary['render_now']:
            del context_dictionary['render_now']
            context_dictionary.update({
                'move_count': move_count,
                'move_count_str': "{:,}".format(move_count),
                'total_points': total_points,
                'total_points_str': "{:,}".format(total_points),
                'visited_room_ids': visited_room_ids,
                })
            return render(request, 'game/home.html', context_dictionary)
        else:
            del context_dictionary['render_now']
            if context_dictionary['current_cavern'].points > 0:
                if not context_dictionary['current_cavern'].id in visited_room_ids:
                    visited_room_ids.append(context_dictionary['current_cavern'].id)
                    total_points += context_dictionary['current_cavern'].points
                    if context_dictionary['current_cavern'].points == 1:
                        points_alert = '<p>Congratulations! This room has 1 point.</p>'
                    else:
                        points_alert = '<p>Congratulations! This room has {0} points.</p>'\
                            .format(context_dictionary['current_cavern'].points)
                    context_dictionary['alert'] = points_alert
                else:
                    points_alert = None
            else:
                points_alert = None
            move_count += 1
            if move_count in (50, 100, 250, 100):
                high_scores = utils.get_high_scores(x=10, move_count=move_count)
                try:
                    cutoff = high_scores[9].total_points
                except:
                    cutoff = -1
                if total_points > cutoff:
                    high_score_alert = '<p>You have a high score of {0} points in {1} moves. \
                        Enter your name or initials to submit to our leaderboard \
                        (this will not interrupt your game): \
                        <input type="text" id="high_score_name" /></p> \
                        <div class="pure-button" id="high_score_submit">Submit</div>'\
                        .format(total_points, move_count)
                    if context_dictionary['alert']:
                        context_dictionary['alert'] += high_score_alert
                    else:
                        context_dictionary['alert'] = high_score_alert
            context_dictionary.update({
                'move_count': move_count,
                'move_count_str': "{:,}".format(move_count),
                'total_points': total_points,
                'total_points_str': "{:,}".format(total_points),
                'visited_room_ids': visited_room_ids,
                })
            return render(request, 'game/home.html', context_dictionary)
        
        
def game_high_scores(request):
    x = 10 #Return top 10 unless you change your mind in the future
    high_scores_50 = utils.get_high_scores(x, move_count=50)
    high_scores_100 = utils.get_high_scores(x, move_count=100)
    high_scores_250 = utils.get_high_scores(x, move_count=250)
    high_scores_1000 = utils.get_high_scores(x, move_count=1000)
    context_dictionary = {
        'high_scores_50': high_scores_50,
        'high_scores_100': high_scores_100,
        'high_scores_250': high_scores_250,
        'high_scores_1000': high_scores_1000,
        }
    return render(request, 'game/high_scores.html', context_dictionary)
    
    
def game_save_high_score(request):
    move_count = int(request.POST.get('move_count'))
    total_points = int(request.POST.get('total_points'))
    name = request.POST.get('name')
    if name == '':
        name = 'anonymous'
    high_score = models.High_Score(
        move_count=move_count, total_points=total_points, name=name
        )
    high_score.save()
    context_dictionary = {
        }
    return render(request, 'game/high_score_saved.html', context_dictionary)

    
## Functions called by main views.
def game_home_get():
    current_cavern = models.Cavern.objects.get(id=1)
    from_cavern = None
    to_caverns = utils.cavern_get_to_caverns(current_cavern, from_cavern)
    move_count = 0
    total_points = 0
    visited_room_ids = []
    alert = None
    context_dictionary = {
        'current_cavern': current_cavern,
        'from_cavern': from_cavern,
        'to_caverns': to_caverns,
        'move_count': move_count,
        'move_count_str': "{:,}".format(move_count),
        'total_points': total_points,
        'total_points_str': "{:,}".format(total_points),
        'visited_room_ids': visited_room_ids,
        'alert': alert,
        }
    return context_dictionary


def cavern_title_get_to_caverns(from_title, current_title):
    from_cavern = models.Cavern.objects.filter(title=from_title)[0]
    current_cavern = models.Cavern.objects.filter(title=current_title)[0]    
    render_now = False
    alert = None
    # this should only happen if user is trying to cheat and hard-code some title to a
        # high-value room. Otherwise we have issues.
    if not current_cavern in utils.cavern_get_to_caverns(from_cavern):
        current_cavern = from_cavern
        from_cavern = None
        to_caverns = utils.cavern_get_to_caverns(current_cavern)
        alert = "There was an error in the last thing you submitted. Please try again."
        context_dictionary = {
            'current_cavern': current_cavern,
            'from_cavern': from_cavern,
            'to_caverns': to_caverns,
            'alert': alert,
            'render_now': render_now,
            }
        return context_dictionary
    else:
        to_caverns = utils.cavern_get_to_caverns(current_cavern, from_cavern)
        context_dictionary = {
            'current_cavern': current_cavern,
            'from_cavern': from_cavern,
            'to_caverns': to_caverns,
            'alert': alert,
            'render_now': render_now,
            }
        return context_dictionary