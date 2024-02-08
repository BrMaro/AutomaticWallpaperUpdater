import os.path
import random
import requests
from bs4 import BeautifulSoup
import ctypes


def get_current_wallpaper():
    # Buffer to store the wallpaper path
    buffer_size = 260  # MAX_PATH
    wallpaper_buffer = ctypes.create_unicode_buffer(buffer_size)

    # Call SystemParametersInfoW to get the current wallpaper path
    result = ctypes.windll.user32.SystemParametersInfoW(0x73, buffer_size, wallpaper_buffer, 0)

    # Check if the call was successful (result is non-zero)
    if result:
        return wallpaper_buffer.value
    else:
        # Handle the case where the call to SystemParametersInfoW failed
        print("Error getting wallpaper.")
        return None


def download_image(imgUrl, filepath):
    try:
        response = requests.get(imgUrl, stream=True)
        response.raise_for_status()

        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Image downloaded to successfully to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def get_ua():
    uastrings = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
    ]

    return random.choice(uastrings)


def main():
    ua = get_ua()
    website_url = "https://4kwallpapers.com/"
    url = "https://4kwallpapers.com/ultrawide-monitor-hd-wallpapers/"
    headers = {"User-Agent": ua}
    response = requests.get(url, headers=headers)
    #storage_folde = "C:\\Users\\Techron\\AppData\\Local\\Packages\\Microsoft.Windows.Photos_8wekyb3d8bbwe\\LocalState\\PhotosAppBackground"
    storage_folder = "C:\\Users\\Techron\\PycharmProjects\\AutomaticWallpaperUpdater\\Downloaded Images"

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.find_all('p', class_="wallpapers__item uwide")
        print(soup.title.text)

        #Download imgs
        for image in images:
            download_link = image.find('a', text="Download")
            if download_link:
                download_link = download_link.get('href')
                img_name = download_link.replace("/images/wallpapers/", "").replace("-", " ").capitalize()
                #print(img_name, download_link)
                if not os.path.isfile(f"C:\\Users\\Techron\\PycharmProjects\\AutomaticWallpaperUpdater\\Downloaded Images\\{img_name}"):
                    download_image(website_url + download_link, os.path.join(storage_folder,img_name))
                else:
                    print("In Library")
            else:
                print("Link NOT Found")

        chosen_image_path = os.path.join(storage_folder,random.choice([f for f in os.listdir(storage_folder) if os.path.isfile(os.path.join(storage_folder,f))]))

        ctypes.windll.user32.SystemParametersInfoW(20, 0, chosen_image_path, 0)

main()
