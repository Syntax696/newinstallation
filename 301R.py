import requests
from concurrent.futures import ThreadPoolExecutor

print('''\
                                                                                    
                                                                                    
██████╗  ██████╗  ██╗
╚════██╗██╔═████╗███║
 █████╔╝██║██╔██║╚██║
 ╚═══██╗████╔╝██║ ██║
██████╔╝╚██████╔╝ ██║
╚═════╝  ╚═════╝  ╚═╝
                     @github.com/Fla4sh
                     @twitter : fla4sh403\
''')

# Meminta input file
file_path = input("Please enter your file: ")

# List untuk menyimpan URL yang valid
valid_urls = []

# Fungsi untuk mengecek URL
def check_url(url):
    try:
        with requests.Session() as session:
            response = session.get(url, allow_redirects=True, timeout=10)  # Timeout dinaikkan menjadi 10 detik
            redirects = response.history[:5]  # Membatasi redirect hanya sampai 5 kali
            num_redirects = len(redirects)
        
        # Jika ada redirect
        if redirects:
            final_url = response.url
            parsed_url = requests.utils.urlparse(url)
            parsed_final_url = requests.utils.urlparse(final_url)
            
            # Cek apakah URL awal dan akhir memiliki domain yang berbeda
            if parsed_url.netloc != parsed_final_url.netloc:
                valid_urls.append(url)
                print(f"The URL {url} redirected {num_redirects} times to {final_url}")
            else:
                print(f"The URL {url} redirected {num_redirects} times to the same domain ({parsed_url.netloc})")
        else:
            print(f"The URL {url} did not redirect")
    except Exception as e:
        print(f"Error occurred while checking URL: {url}")
        print(e)

# Membuka file yang berisi URL dan menuliskan URL valid ke file 'valid_urls.txt'
with open(file_path, "r", encoding="utf-8") as file, open("valid_urls.txt", "w") as valid_file, ThreadPoolExecutor(max_workers=10) as executor:
    # Menjalankan fungsi check_url untuk setiap URL dalam file
    futures = [executor.submit(check_url, url.strip()) for url in file]
    
    # Menunggu semua proses selesai
    for future in futures:
        future.result()

    # Menulis URL valid ke file 'valid_urls.txt'
    valid_file.write("\n".join(valid_urls))

print(f"Valid URLs saved to valid_urls.txt")
