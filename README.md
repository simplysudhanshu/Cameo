# \ __ - CAMEO - __ /
Implementation of cards game CAMEO using python. (Multiplayer over internet.)
--
Basic Requirements:
> 1) Python 3.x
> 2) [Selenium package](https://pypi.org/project/selenium/)
> 3) [Latest Google Chrome](https://www.google.com/chrome/)

`The chromedriver provided works with Chrome vertsion 83.0. If your version mismatches, 
either update your chrome via the link above, or get appropriate chromedriver` [here.](https://chromedriver.chromium.org/)
***
*Rules of CAMEO game :*
> Motive : Minimise the score of your cards.

1. Each player gets 5 cards, from which you are allowed to see the first two cards.
2. At each turn, you can pick a card from the deck and swap with any of your cards, or you can `burn` a set of your cards, whose total should match the score of the card on top of the stack. (:grey_exclamation:Face cards can be burnt using face cards only.)
3. There are a set of **Power Cards**: (These powers can be availed whenever you place a power card on stack)
    1) *7 / 8* - You can see any one of your cards.
    2) *9 / 10* - You can see any one card of someone else.
    4) *Jack / Queen [J / Q]* - You can swap any one of your cards with one card of anyone else, without look at the cards.
    5) *King [K]* - You can look one card of your cards and one card of anyone else and swap them if you want.
4. While calculating the scores, both the *Red Kings (Diamond and Heart)* have 0 value.
5. If you think you have the lowest score amongst all the players, you can invoke CAMEO!, upon which all the other players will be allowed to play one hand each and at the end of whole circle, scores will be calculated for every player. In this last round, no player can look, swap or shuffle the cards of the player who has invoked cameo.

> The player with lowest score is declared WINNER!
