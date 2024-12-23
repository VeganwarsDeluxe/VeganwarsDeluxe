import random

from VegansDeluxe.core import NPC, Session, AttachedAction, DecisiveAction, ActionTag, OwnOnly, ActionManager

quotes = """Kozych.
Three paths lead to knowledge: the path of reflection is the noblest path, the path of imitation is the easiest path, and the path of experience is the bitterest path.
Even in the company of two people, I will certainly find something to learn from them. I will try to imitate their virtues, and I will learn from their shortcomings.
If you hate, it means you have been defeated.
Only the wisest and the stupidest are not susceptible to learning.
In a country where there is order, be bold in both actions and speech. In a country where there is no order, be bold in actions, but cautious in speech.
He who, turning to the old, is able to discover the new, is worthy of being a teacher.
Before you take revenge, dig two graves.
He who cannot instruct his family to do good cannot learn himself.
Give instructions only to those who seek knowledge, having discovered their ignorance.
To study and, when the time comes, to apply what you have learned to action - isn't that wonderful!
Happiness is when you are understood, great happiness is when you are loved, true happiness is when you love.
It is difficult to meet a person who, having devoted three years of his life to study, would not dream of occupying a high position.
In fact, life is simple, but we persistently complicate it.
At fifteen, I turned my thoughts to study. At thirty, I gained independence. At forty, I got rid of doubts. At fifty, I knew the will of heaven. At sixty, I learned to distinguish truth from untruth. At seventy, I began to follow the desires of my heart.
Intemperance in small things will ruin a great cause.
Forget insults. But never forget kindness.
Only when the cold comes, it becomes clear that the pines and cypresses are the last to lose their attire.
It is very easy to recognize a happy person. He seems to radiate an aura of calm and warmth, moves slowly, but manages to do everything, speaks calmly, but everyone understands him. The secret of happy people is simple - it is the absence of tension.
People in ancient times did not like to talk much. They considered it a shame for themselves not to keep up with their own words.
If you want to succeed, avoid six vices: drowsiness, laziness, fear, anger, idleness and indecision.
We take advice in drops, but give it out in buckets.
Where patience ends, endurance begins.
A precious stone cannot be polished without friction. Likewise, a person cannot become successful without a sufficient number of difficult attempts.
Beware of those who want to impute a sense of guilt to you, for they thirst for power over you.
A noble man makes demands on himself, a base man makes demands on others.
Sometimes it is worth making a mistake, if only for the sake of knowing why it should not have been made.
You can overcome bad habits only today, not tomorrow.
The man who is at the very top of the mountain did not fall there from the sky.
Three things never return - time, words, opportunity. Therefore: do not waste time, choose your words, do not miss an opportunity.
To respect every person as yourself, and to treat him as we want to be treated - there is nothing higher than this.
Choose a job you like, and you will never have to work a day in your life.
If you do not have bad thoughts, there will be no bad deeds.
I am not upset if people do not understand me - I am upset if I do not understand people.
A worthy person does not follow in the footsteps of other people.
Try to be at least a little kinder, and you will see that you will not be able to commit a bad deed.
Visiting and listening to evil people is already the beginning of an evil deed.
In ancient times, people studied in order to improve themselves. Nowadays, people study to surprise others.
Silence is a great friend who will never betray.
You can curse the darkness all your life, or you can light a small candle.
A noble man blames himself, a small man blames others.
When misfortune comes, a man gave birth to it, when happiness comes, a man raised it.
An angry man is always full of poison.
There is beauty in everything, but not everyone is given to see it.
A respectful son is one who upsets his father and mother only with his illness.
A noble man is serene in his soul. A base man is always worried.
Only a truly humane person is capable of both loving and hating.
If they spit in your back, it means you are ahead.
A noble man knows only duty, a base man knows only benefit.
Not he who has never fallen is great, but he who has fallen and risen is great.
Pay for evil with sincerity, and for good, pay with good.
If nature overshadows education in a man, the result will be a savage, and if education overshadows nature, the result will be a scholar of the scriptures. Only he in whom nature and education are in balance can be considered a worthy man.
To send men to war untrained is to betray them.
How can we know what death is when we do not yet know what life is?
In assessing worldly affairs, a noble man does not reject or approve of anything, but measures everything with justice.
A wise man does not do to others what he does not want done to him.
When you do not know words, you have nothing with which to know people.
Do not worry about not being known. Worry about whether you are worthy of being known.
Lead the people with dignity, and they will respect you. Treat the people kindly, and they will work hard. Elevate the virtuous and instruct the uneducated, and people will trust you.
To fail to speak to a person who is worthy of conversation is to lose a person. And to speak to a person who is not worthy of conversation is to lose words. The wise man loses neither people nor words.
To fail to speak to a person who is worthy of conversation is to lose a person. And to speak to a person who is not worthy of conversation is to lose words. The wise man loses neither people nor words.
Sometimes we see many things, but do not notice the main thing.
The wise man is ashamed of his shortcomings, but is not ashamed to correct them.
I do not understand how one can deal with a person who cannot be trusted? If the cart has no axle, how can one ride on it?
Do not have friends who are inferior to you in morality.
Study as if you constantly feel the lack of your knowledge, and as if you are constantly afraid of losing your knowledge.
If a person is firm, decisive, simple and taciturn, then he is already close to humanity.
When, having made a mistake, you do not correct it, this is called making a mistake.
It is beautiful where mercy resides. How can you achieve wisdom if you do not live in its lands?
Learning without reflection is useless, but reflection without learning is dangerous.
When the paths are not the same, do not make plans together.
He is not great who never fell, but he is great - who fell and got up.
You cannot look down on young people. It is very likely that, having matured, they will become outstanding men. Only he who has achieved nothing, having lived to forty or fifty years, does not deserve respect.
Life is simple, but we insist on making it complicated.
When you are cold to your parents, admonish them as gently as possible. If your advice does not have any effect, continue to be respectful and humble. Even if you are annoyed in your soul, do not express your dissatisfaction.
Happiness is when you are understood, great happiness is when you are loved, true happiness is when you love.
He who does not think about distant difficulties is sure to face near troubles.
If you hate, it means you have been defeated.
People want wealth and glory for themselves; if both cannot be obtained honestly, they should be avoided.
It does not matter how slowly you go, as long as you do not stop.
When they proceed only from profit, they multiply malice.
Never make friends with a person who is no better than yourself.
If you are straightforward, then everything will be done without orders. And if you yourself are not direct, then they will not obey, even if they are ordered.
When you are angry, think about the consequences.
If you are overly zealous in service, you will lose the favor of the sovereign. If you are overly cordial in friendship, you will lose the favor of friends.
If it is obvious that goals cannot be achieved, do not adjust goals, adjust actions.
A noble man knows his superiority, but avoids rivalry. He gets along with everyone, but does not collude with anyone.
Whatever you do in life, do it with all your heart.
Having learned the truth in the morning, you can die in the evening.
Observe a person's behavior, delve into the reasons for his actions, look closely at him during leisure hours. Will he then remain a mystery to you?
Beautiful speeches harm morality. When there is no desire to do small things, this harms big plans.
Noble people live in harmony with others, but do not follow others; base people follow others, but do not live in harmony with them.
He who is full of mercy certainly has courage.
Blessed is he who knows nothing: he does not risk being misunderstood.
When it is clear what morality consists of, then everything else will be clear.
When outside the home, behave as if you were receiving honored guests. When using people's services, behave as if you were performing a solemn ceremony. Do not do to others what you would not wish for yourself. Then there will be no discontent in the state or in the family.
The bird chooses the tree. How can the tree choose the bird?
We trust our eyes - but they cannot be trusted; we rely on our hearts - but we should not rely on them either. Remember, then, disciples: it is truly not easy to know a person!
The wise man knows no worries, the humane man knows no cares, the brave man knows no fear
When you meet a worthy man, think about how to be equal to him. When you meet a low man, look closely at yourself and judge yourself.
A noble man is direct and firm, but not stubborn."""


class Confucius(NPC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hp = 1
        self.max_hp = 1

        self.name = "Confucius"

    async def choose_act(self, session: Session, action_manager: ActionManager):
        action_manager.queue_action(session, self, ConfuciusQuote.id)


@AttachedAction(Confucius)
class ConfuciusQuote(DecisiveAction):
    id = 'skip'
    name = "Confucius"
    target_type = OwnOnly()
    priority = 2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.SKIP]

    async def func(self, source, target):
        self.session.say(f"💬|{source.name}: {random.choice(quotes.split('\n'))}")
