import os, time, subprocess, threading, requests
from colorama import init, Fore
import speedtest

# Initialize colorama
init(autoreset=True)

class NetAxe:
    def __init__(self):
        # Initialize title and any other setup items
        self.setup()
        self.sniffer_thread = None  # Track the sniffer thread

    def setup(self):
        # Set the console window title and display the banner
        os.system("cls")
        os.system("title NetAxe")
        self.banner()
        self.menu()

    def banner(self):
        # Display the banner in light black color
        print(Fore.LIGHTBLACK_EX + r'''
                                         _   _      _    ___           
                                        | \ | |    | |  / _ \          
                                        |  \| | ___| |_/ /_\ \_  _____ 
                                        | . ` |/ _ \ __|  _  \ \/ / _ \
                                        | |\  |  __/ |_| | | |>  <  __/
                                        \_| \_/\___|\__\_| |_/_/\_\___|                                   
                                    _______________________________________ 
                               ''')

    def menu(self):
        # Main menu functionality
        while True:
            print(Fore.LIGHTBLACK_EX + "[01] > Exit             [05] > Pinger")
            print(Fore.LIGHTBLACK_EX + "[02] > Reveal IP        [06] > IP Geolocator")
            print(Fore.LIGHTBLACK_EX + "[03] > Get WiFi Info    [07] > DNS Lookup")
            print(Fore.LIGHTBLACK_EX + "[04] > Get All WiFis    [08] > Network Speed Test")
            inp = input(Fore.LIGHTBLACK_EX + "> ")
            if inp == "1":
                print(Fore.GREEN + "[+] Exiting...")
                time.sleep(1)
                exit()  # Exit the loop and finish the program
            elif inp == "2":
                self.reveal_ip()  # Call the Reveal IP function
            elif inp == "3":
                self.get_wifi_info()  # Call the Get WiFi Info function
            elif inp == "4":
                self.get_all_wifis()  # Call the Get All WiFis function
            elif inp == "5":
                self.pinger()  # Call the Pinger function
            elif inp == "6":
                self.ip_geolocator()  # Call the IP Geolocator function
            elif inp == "7":
                self.dns_lookup()  # Call the DNS Lookup function
            elif inp == "8":
                self.network_speed_test()  # Call the Network Speed Test function
            else:
                print(Fore.RED + "[-] Invalid option.")
                time.sleep(1)
            
            self.setup()

    def reveal_ip(self):
        os.system("cls")
        self.banner()
        print(Fore.YELLOW + "[?] Getting Your IP Address...")
        time.sleep(1)
        try:
            # Run ipconfig command and decode the output
            result = subprocess.check_output("ipconfig", encoding="utf-8")
            
            # Extract the IP address from the ipconfig output
            for line in result.splitlines():
                if "IPv4" in line:  # This filters out the IPv4 address
                    ip_address = line.split(":")[1].strip()
                    print(Fore.GREEN + f"[+] IP Address: {ip_address}")
                    break
            else:
                print(Fore.RED + "[-] Unable to find IP address.")
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "[-] Error occurred while running ipconfig.")

        # Pause to view result
        input(Fore.LIGHTBLACK_EX + "[Press Enter to go back]")

    def get_wifi_info(self):
        os.system("cls")
        self.banner()
        wifi_name = input(Fore.YELLOW + "[?] Enter WiFi name: ")
        print(Fore.YELLOW + f"[?] Fetching WiFi info for \"{wifi_name}\"...")
        try:
            # Run netsh wlan show profile to get WiFi details
            result = subprocess.check_output(f'netsh wlan show profile name="{wifi_name}" key=clear', encoding="utf-8")
            print(Fore.GREEN + result)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "[-] Error occurred while fetching WiFi info. Make sure the WiFi name is correct.")

        # Pause to view result
        input(Fore.LIGHTBLACK_EX + "[Press Enter to go back]")

    def get_all_wifis(self):
        os.system("cls")
        self.banner()
        print(Fore.YELLOW + "[?] Fetching all available WiFi profiles...")
        try:
            # Run netsh wlan show profiles to list all WiFi networks
            result = subprocess.check_output("netsh wlan show profiles", encoding="utf-8")
            print(Fore.GREEN + result)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "[-] Error occurred while fetching WiFi profiles.")

        # Pause to view result
        input(Fore.LIGHTBLACK_EX + "[Press Enter to go back]")

    def pinger(self):
        os.system("cls")
        self.banner()

        # Pinger functionality
        ip = input(Fore.YELLOW + "[?] Enter the IP address to ping: ")
        num_threads = int(input(Fore.YELLOW + "[?] Enter the number of threads to run: "))  # Input thread count
        num_pings = int(input(Fore.YELLOW + "[?] Enter the number of pings per thread: "))  # Input number of pings per thread

        print(Fore.YELLOW + f"Starting {num_pings} pings per thread to {ip} with {num_threads} threads...")

        stop_event = threading.Event()

        def ping_target(ip, num_pings):
            for i in range(num_pings):
                if stop_event.is_set():
                    break
                # Run the ping command
                response = subprocess.run(
                    ["ping", "-n", "1", ip],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                # Check the response
                if response.returncode == 0:
                    print(Fore.GREEN + f"Success: {ip} is reachable.")
                else:
                    print(Fore.RED + f"Failure: {ip} is not reachable.")
                
                # Sleep a tiny bit to allow the event to be checked frequently
                time.sleep(0.1)

        # Create and start threads
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=ping_target, args=(ip, num_pings))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        input(Fore.LIGHTBLACK_EX + "[Press Enter to go back]")

    def ip_geolocator(self):
        os.system("cls")
        self.banner()
        ip = input(Fore.YELLOW + "[?] Enter the IP address to geolocate: ")
        try:
            # Using a free API for IP geolocation
            response = requests.get(f"http://ip-api.com/json/{ip}")
            data = response.json()
            
            if data["status"] == "fail":
                print(Fore.RED + f"[-] Failed to retrieve geolocation for {ip}.")
            else:
                print(Fore.GREEN + f"[+] Geolocation for IP: {ip}")
                print(Fore.GREEN + f"Country: {data['country']}")
                print(Fore.GREEN + f"Region: {data['regionName']}")
                print(Fore.GREEN + f"City: {data['city']}")
                print(Fore.GREEN + f"Latitude: {data['lat']}")
                print(Fore.GREEN + f"Longitude: {data['lon']}")
        except Exception as e:
            print(Fore.RED + "[-] Error occurred while geolocating the IP.")

        input(Fore.LIGHTBLACK_EX + "[Press Enter to go back]")

    def dns_lookup(self):
        os.system("cls")
        self.banner()
        domain = input(Fore.YELLOW + "[?] Enter the domain name to lookup: ")
        try:
            # Using the requests module to query DNS records (A, MX, CNAME)
            response = subprocess.check_output(f"nslookup {domain}", encoding="utf-8")
            print(Fore.GREEN + f"[+] DNS Records for {domain}:")
            print(Fore.GREEN + response)
        except subprocess.CalledProcessError as e:
            print(Fore.RED + "[-] Error occurred while performing DNS lookup.")

        input(Fore.LIGHTBLACK_EX + "[Press Enter to go back]")

    def network_speed_test(self):
        os.system("cls")
        self.banner()
        print(Fore.YELLOW + "[?] Testing network speed... This may take a few seconds.")
        
        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        ping = st.results.ping

        print(Fore.GREEN + f"[+] Download speed: {download_speed:.2f} Mbps")
        print(Fore.GREEN + f"[+] Upload speed: {upload_speed:.2f} Mbps")
        print(Fore.GREEN + f"[+] Ping: {ping} ms")

        input(Fore.LIGHTBLACK_EX + "[Press Enter to go back]")

# Create instance of NetAxe and run
netaxe = NetAxe()