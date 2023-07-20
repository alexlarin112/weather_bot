from PIL import Image, ImageDraw, ImageFont
from os.path import join


class WeatherNowImage:
    def __init__(self):
        self.__im = Image.new('RGB', (1080, 1080), color='#40CFFF')
        self.__basic_font_path = './static/fonts/BIZUDGothic-Bold.ttf'
        self.__font_descr = ImageFont.truetype(self.__basic_font_path, size=30)
        self.__font_city_name = ImageFont.truetype(self.__basic_font_path, size=40)
        self.__font_params = ImageFont.truetype(self.__basic_font_path, size=50)
        self.__font_temp = ImageFont.truetype(self.__basic_font_path, size=300)
        self.__font_date = ImageFont.truetype(self.__basic_font_path, size=40)

        self.__image = ImageDraw.Draw(self.__im)

    def create_weather_image(self, name: str, date: str,  temperature: str | int, description: str,
                             uv: str, uv_time: str, uv_max: str, uv_max_time: str, pressure: str | int,
                             humidity: str | int, filename: str | int, icon: str) -> None:

        self.__draw_city_name(name)
        self.__draw_date(date)
        self.__draw_temperature(temperature)
        self.__draw_weather_description(description)
        self.__draw_uv_index(uv, uv_time)
        self.__draw_uv_max(uv_max, uv_max_time)
        self.__draw_pressure(pressure)
        self.__draw_humidity(humidity)
        self.__draw_weather_icon(icon)
        self.__save_image(filename)

    def __save_image(self, filename: int) -> None:
        path = join('.', 'media', f'{(str(filename))}.png')
        self.__im.save(path)

    def show_image(self):
        self.__im.show()

    def __draw_city_name(self, name: str) -> None:
        self.__image.text(
            (30, 90),
            name,
            font=self.__font_city_name,
            fill='white'
            )

    def __draw_date(self, date: str) -> None:
        self.__image.text(
            (800, 90),
            date,
            font=self.__font_date,
            fill='white'
            )

    def __draw_temperature(self, temperature: str) -> None:

        #   линии вокруг температуры
        self.__image.line((0, 220, 1080, 220), fill='white', width=5)
        self.__image.line((0, 600, 1080, 600), fill='white', width=5)

        self.__image.text(
            (240, 270),
            text='+' + str(temperature) + '°' if int(temperature) > 0 else str(temperature) + '°',
            font=self.__font_temp,
            fill='white'
            )

    def __draw_weather_description(self, description: str) -> None:
        self.__image.text(
            (30, 650),
            description,
            font=self.__font_descr,
            fill='white'
            )

    def __draw_uv_index(self, uv: str, uv_time: str) -> None:
        path = join('.', 'static', 'images', 'params_icons', 'uv.png')
        uv_image = Image.open(path)
        self.__im.paste(uv_image, (30, 735), uv_image)

        self.__image.text(
            (90, 730),
            f' uv в {uv_time}: {int(uv)}',
            font=self.__font_params,
            fill='white'
            )

    def __draw_uv_max(self, uv_max: str, uv_max_time: str) -> None:
        path = join('.', 'static', 'images', 'params_icons', 'uv_max.png')
        uv_max_image = Image.open(path)
        self.__im.paste(uv_max_image, (30, 810), uv_max_image)
        self.__image.text(
            (90, 810),
            f' uv-max в {uv_max_time}: {int(uv_max)}',
            font=self.__font_params,
            fill='white'
            )

    def __draw_pressure(self, pressure: str | int) -> None:
        path = join('.', 'static', 'images', 'params_icons', 'pressure.png')
        pressure_image = Image.open(path)
        self.__im.paste(pressure_image, (30, 890), pressure_image)
        self.__image.text(
            (90, 890),
            f' {pressure} мм.рт.ст.',
            font=self.__font_params,
            fill='white'
            )

    def __draw_humidity(self, humidity: str | int) -> None:
        path = join('.', 'static', 'images', 'params_icons', 'humidity.png')
        humiditiy_image = Image.open(path)
        self.__im.paste(humiditiy_image, (30, 970), humiditiy_image)
        self.__image.text(
            (90, 970),
            f' {humidity}%',
            font=self.__font_params,
            fill='white'
        )

    def __draw_weather_icon(self, icon: str) -> None:
        path = join('.', 'static', 'images', 'weather_icons', f'{icon}.png')
        icon_image = Image.open(path)
        icon_image = icon_image.resize((300, 300))
        self.__im.paste(icon_image, (700, 700), icon_image)


# image = WeatherNowImage()
# image.create_weather_image('Санкт-Петербург', '20:05 29.06', '20', 'Пасмурно', '6',
#                            '20:05', "10", '13:05', 750, 21, 123, '03n')
# image.show_image()



#

#
# draw_text.text(
#     (30, 990),
#     'Скорость ветра: 5 м/c',
#     font=font_params,
#     fill=('#1C0606')
#     )




