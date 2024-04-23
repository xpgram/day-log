"""
Manages this line:
[                                                                      : Today 3,2 (3,3)  Rem 27,1 ]
 
[ Show which date ranges?                                              : Today 3,2 (3,3)  Rem 27,1 ]

[                                                                          : Banked 11,2  Owed 2,1 ]

[ Updated view to Compact.                                                 : Banked 11,2  Owed 2,1 ]

I think this was originally meant to manage all my banked time for me, but I'm not sure that's
realistic. I do a lot of editing to it.

[ ] Displays tally totals
  - Keeps me appraised of the day spent and the week remaining. (Or the day remaining?)
  - Displays other tallies, like banked time.
[ ] Displays messages to the user.
  - Some messages are timed and will disappear on their own.
  - Some messages are questions and will not disappear.
  - If timed messages are queued, they'll run through one-by-one, like an event log in a video game.
      - Messages are per user-command, yes? This shouldn't be necessary, but eh.
[ ] Knows what to display via the event dispatch system.
  - Updated time totals are obtained via event.
  - Messages and questions to display are updated via event.
"""

class Marquee:

  dayRemainingMax = "8,0"
  dayRemainingMin = "8,0"
  weekRemaining = "40,0"

  def display(self):
    # TODO For demo purposes
    dayHasTimeRange = (self.dayRemainingMin != self.dayRemainingMax)
    dayRemainingParens = f' ({self.dayRemainingMin})' if dayHasTimeRange else ''
    dayRemaining = f'Today {self.dayRemainingMax}{dayRemainingParens}'

    weekRemaining = f'Rem {self.weekRemaining}'

    metrics = f' : {dayRemaining}  {weekRemaining}'

    fullSize = 100
    innardsSize = fullSize - len('[  ]') - len(metrics)
    message = "What would you like to do?"
    whitespaceSize = innardsSize - len(message)

    whitespace = ' ' * whitespaceSize

    print(f'[ {message}{whitespace}{metrics} ]')


m = Marquee()
m.display()