import subprocess

def list_wifi_networks():
    """Получает список доступных Wi-Fi сетей."""
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID,SIGNAL', 'dev', 'wifi'], capture_output=True, text=True)
        networks = result.stdout.splitlines()
        print("Доступные Wi-Fi сети:")
        for i, network in enumerate(networks, 1):
            ssid, signal = network.split(':')
            print(f"{i}. {ssid} (Сила сигнала: {signal}%)")
        return networks
    except Exception as e:
        print(f"Ошибка при получении списка сетей: {e}")
        return []

def connect_to_wifi(ssid, password):
    """Подключается к указанной Wi-Fi сети."""
    try:
        subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], check=True)
        print(f"Подключение к сети {ssid} успешно!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при подключении к сети {ssid}: {e}")

def disconnect_wifi():
    """Отключается от текущей Wi-Fi сети."""
    try:
        subprocess.run(['nmcli', 'dev', 'disconnect', 'iface', 'wlan0'], check=True)
        print("Отключение от Wi-Fi выполнено успешно.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при отключении от Wi-Fi: {e}")

def show_current_connection():
    """Показывает текущее подключение."""
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE', 'connection', 'show', '--active'], capture_output=True, text=True)
        connections = result.stdout.splitlines()
        if connections:
            print("Текущие подключения:")
            for conn in connections:
                name, conn_type = conn.split(':')
                print(f"- {name} ({conn_type})")
        else:
            print("Нет активных подключений.")
    except Exception as e:
        print(f"Ошибка при получении текущих подключений: {e}")

def main():
    print("Менеджер Wi-Fi сетей для Linux")
    while True:
        print("\nВыберите действие:")
        print("1. Показать доступные Wi-Fi сети")
        print("2. Подключиться к Wi-Fi сети")
        print("3. Отключиться от Wi-Fi")
        print("4. Показать текущее подключение")
        print("5. Выйти")
        choice = input("Ваш выбор: ")

        if choice == "1":
            list_wifi_networks()
        elif choice == "2":
            ssid = input("Введите SSID сети для подключения: ")
            password = input("Введите пароль: ")
            connect_to_wifi(ssid, password)
        elif choice == "3":
            disconnect_wifi()
        elif choice == "4":
            show_current_connection()
        elif choice == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
