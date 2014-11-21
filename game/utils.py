from game import models
    
def get_high_scores(x, move_count):
    high_scores = models.High_Score.objects.filter(move_count=move_count)\
        .order_by('-total_points', 'created_at')[:x]
    return high_scores
    
def cavern_get_to_caverns(cavern, from_cavern=None):
    to_caverns = cavern.connections.all()
    from_caverns = models.Cavern.objects.filter(connections=cavern)
    to_caverns = list(set(to_caverns).union(set(from_caverns)) - set([from_cavern]))
    return to_caverns