import asyncio
import os
import subprocess

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

profile_path = os.path.expandvars(
    r"C:\\Users\\Lenovo\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Data\\Browser\\profile.default"
)
options = Options()
options.set_preference("profile", profile_path)
service = Service(
    # os.path.expandvars(r"%USERPROFILE%\Desktop\Tor Browser\Browser\firefox.exe"),
    executable_path=GeckoDriverManager().install()
)

options.set_preference("network.proxy.type", 1)
options.set_preference("network.proxy.socks", "127.0.0.1")
options.set_preference("network.proxy.socks_port", 9050)
options.set_preference("network.proxy.socks_remote_dns", False)


async def main():
    async def cleanup():
        driver.quit()
        print(torexe.pid)
        torexe.kill()

    try:
        # https://stackoverflow.com/a/62686067/8608146
        torexe = subprocess.Popen(
            os.path.expandvars(
                r"C:\\Users\\Lenovo\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe"
            )
        )
        driver = Firefox(service=service, options=options)
        # driver.get("https://check.torproject.org")
        driver.get("https://whatismyipaddress.com/")
        driver.save_screenshot("screenshot3.png")
    except Exception as e:
        print(e, type(e))
    finally:
        await cleanup()


if __name__ == "__main__":
    asyncio.run(main())