import random
import time

character_status = {
    "status": "character",
    "health_point": random.randint(500, 700),
    "armor_point": random.randint(300, 500),
    "attack_status": 0
}

bos_status = {
    "status": "bos",
    "health_point": random.randint(500, 700),
    "armor_point": random.randint(300, 500),
    "attack_status": 0
}


def show_status(status):
    print("=" * 20)
    print(f"status       : {status['status']}")
    print(f"health_point : {status['health_point']}")
    print(f"armor_point  : {status['armor_point']}")
    print(f"attack_status: {status['attack_status']}")
    print("=" * 20)


print("INITIALIZE")
show_status(character_status)
show_status(bos_status)

while True:
    print("1. Attach")
    print("2. Healing")
    print("3. Surrender")

    input_user = int(input("Input: "))
    if input_user == 1:
        character_status["attack_status"] = random.randint(100, 200)
        attack_value = character_status["attack_status"]
        print(f"Menyerang si Bos dengan Attack {attack_value}")
        time.sleep(1.0)
        bos_status["health_point"] -= attack_value
        if bos_status["health_point"] < 0:
            bos_status["health_point"] = 0
            print("Bos telah Mati")
            break
        show_status(bos_status)

        bos_status["attack_status"] = random.randint(100, 200)
        attack_value_bos = bos_status["attack_status"]
        print(f"Bos Menyerang kita dengan Attack {attack_value_bos}")
        time.sleep(1.0)
        character_status["health_point"] -= attack_value_bos
        if character_status["health_point"] < 0:
            character_status["health_point"] = 0
            print("Character telah Mati")
            break
        show_status(character_status)
    elif input_user == 2:
        pass
    elif input_user == 3:
        print("Character telah Menyerah, Bos Menang")
        break
    else:
        print("Masukan input yang valid")
