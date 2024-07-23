from util import blackjack
import inspect


if __name__ == "__main__":
    
    game = blackjack.Blackjack()
    while(True):
        game.play_hand()

    # print(f"qualname: {blackjack.Blackjack.Blackjack2.__qualname__}")
    # print(f"module: {blackjack.Blackjack.__module__}")
    # print(f"name: {blackjack.Blackjack.__name__}")
    # print(f"annotations: {blackjack.Blackjack.__annotations__}")