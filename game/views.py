from django.shortcuts import render
from game import models

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
        ## TO-DO --> Always ship a csrf tag ###
        current_cavern = models.Cavern.objects.get(id=2)
        from_cavern = None
        to_caverns = current_cavern.get_to_caverns(from_cavern)
        move_count = 0
        total_points = 0
        visited_room_ids = []
        context_dictionary = {
            'current_cavern': current_cavern,
            'from_cavern': from_cavern,
            'to_caverns': to_caverns,
            'move_count': move_count,
            'total_points': total_points,
            'visited_room_ids': visited_room_ids,
            }
        return render(request, 'game/home.html', context_dictionary)