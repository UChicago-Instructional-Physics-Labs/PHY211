import numpy as np

class particle:
    def __init__(self, xpos, ypos):
        self.x = xpos
        self.y = ypos
        self.t = 1 
    def __str__(self):
        return "[%s, %s, %s]\n" % (self.x,self.y,self.t)
            # This defines a particle as something that has an x and y position as well as an elapsed lifetime t
            # __str__ tells Python how to show us this data when using a print command

class particle_list:
    def __init__(self):
        self.particles = []
        self.decayed_particles = []
            # particle lists are what they sound like: a list of particles
            # decayed_particles stores all the particles that have already decayed, so that Python doesn't have to loop through them as much.
    def num_particles(self):
        return len(self.particles)
    def get_x(self):
        tx = []
        for item in self.particles:
            tx.append(item.x)
        return tx
            # returns a list of the x coordinates of all particles that haven't decayed
    def get_y(self):
        ty = []
        for item in self.particles:
            ty.append(item.y)
        return ty
    def get_t(self):
        tt = []
        for item in self.particles:
            tt.append(item.t)
        for item in self.decayed_particles:
            tt.append(item.t)
        return tt
            # returns a list of the elapsed lifetimes of all particles
    def get_paired_xy(self):
        return np.transpose([self.get_x(),self.get_y()])
            # returns particle coorinates as a list of x-y pairs
    def add_particle(self,new_x,new_y):
        self.particles.append(particle(new_x,new_y))
            # defines a function to add a new particle to the list
    def __repr__(self):
        return "%s \n" % (self.particles)
    def decay(self,rate):
        for item in self.particles:
            if(np.random.rand() <= rate):
                self.decayed_particles.append(item)
                self.particles.remove(item)
            else:
                item.t = item.t +1
            # central function: when given a rate, this iterates through all particles and either has them decay or
            # adds 1 to the ellapsed lifetime.
    def create(self,rate):
        if(np.random.rand() <= rate):
            self.add_particle(1+np.random.rand()*8,1+np.random.rand()*8)
            # defines how to add particles at a particular rate
print("Setup done")

import time
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


lst = particle_list()

plt.ion() 
    # makes the plot interactive, needed for animation
fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1,figsize=(8,8)) 
    # Alternative way of initializing subplots


ax2.set_ylabel('Counts')


sc = ax1.scatter(lst.get_x(),lst.get_y())
ax1.set_xlim([0, 10])
ax1.set_ylim([0, 10])
ax1.set_aspect('equal')
    # setting up a scatter plot of particles

sc2 = ax2.hist(lst.get_t())


lst.add_particle(1+np.random.rand()*8,1+np.random.rand()*8)
    # adds a sintle particle to get things started off, where 1 > x > 9 and 1 > y > 9
    # the position doesn't really do anything, it is just there for visualization purposes.
plt.draw() 

while (time.time() < t_end):
    for i in range(frame_skip):
        lst.create(add_chance)
        lst.decay(decay_chance)
        #this is the core part of the loop: maybe add a particle and then check for decays
    sc.set_offsets(lst.get_paired_xy())
        # this sets up the positions of particles in the scatterplot.
    ax2.cla()
    ax2.set_ylabel('Counts')
        # clears off the lifetime plot, resets labels
    time_data = lst.get_t()
    dat,bins = np.histogram(time_data,bins=hist_bins)
        # generates histogram data from the particle lifetimes
    ax2.errorbar(bins[0:-1],dat,np.sqrt(dat),fmt='.r',alpha=0.5)
        # makes a plot of the binned data, with square root N error bars
        # note that since numpy's histogram gives back one more bin value that data point, we need to chop one off the array
        # hence the [0:-1] notation
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))      
        # this line force the y axis tics to be integers.  Not critical.
    plt.title("Time remaining:%i" % int(t_end - time.time()))
        # sets the title to the remaining time the sim is running
    fig.canvas.draw()
    plt.pause(0.01)
        # pause is needed, otherwise the visuals never refresh
