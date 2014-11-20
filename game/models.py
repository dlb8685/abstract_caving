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
    title = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    link = models.CharField(max_length=1000, blank=True, default="")
    color = models.ForeignKey(Color)
    points = models.SmallIntegerField(default=0)
    is_entrance = models.BooleanField(default=False)
    connections = models.ManyToManyField("self")
    
    def __str__(self):
        return self.title[:50]
        
    def get_to_caverns(self, from_cavern=None):
        to_caverns = self.connections.all()
        to_caverns = list(set(to_caverns) - set([from_cavern]))
        return to_caverns