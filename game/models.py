from django.db import models

class Color(models.Model):
    '''
    Normalize Color so you can easily adjust it
    '''
    color = models.CharField(max_length=200, blank=True, default="")

class Cavern(models.Model):
    '''
    Fundamental unit. 
    Each of these has: 
        - Title
        - Description (i.e. some text on a subject)
        - Link (external link)
        - Color (in hex, represented as a 7 character taxt) 
        - Points (point value of visiting this cavern, somewhere between 0-10)
        - Is Entrance? (this will be true for one Cavern, where id=1, otherwise false)
        - Many-to-many relationship with other Caverns, to build out the network of them
    '''
    title = models.TextField(db_index=True, blank=True, default="")
    description = models.TextField(blank=True, default="")
    link = models.CharField(max_length=1000, blank=True, default="")
    color = models.ForeignKey(Color)
    points = models.SmallIntegerField(default=0)
    is_entrance = models.BooleanField(default=False)
    connections = models.ManyToManyField("self")
    
    def __str__(self):
        return self.title[:50]


class High_Score(models.Model):
    '''
    Save high scores and index the score such that you can quickly create Top 10 lists.
    Tiebreaker will be created time.
    User can enter their name, or it will default to unknown.
    '''
    move_count = models.SmallIntegerField(db_index=True)
    total_points = models.SmallIntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=25, blank=True, default="anonymous")