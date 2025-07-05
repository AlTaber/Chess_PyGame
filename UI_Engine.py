#       Набор инструментов для реализации базового пользовательского интерфейса

import pygame as pg
import os
import sys

# Функция открытия изображений для последующего преобразовывания в спрайты
def load_image(name, colorkey=None):
    fullname = os.path.join('Assets/Images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Класс кнопки для виджета
class Button:
    def __init__(self, parent, position, size,
                icon_name = "",
                text = "",
                action = None):
        self.parent = parent # Ссылка на родительский виджет

        self.position = position # Позиция кнопки относительно виджета
        self.size = size # Размер кнопки

        self.icon_name = icon_name # Название файла с иконкой для кнопки
        self.text = text # Текст который будет отображаться на кнопке

        self.is_toggled = False # Если кнопка переключает какую нибудь настройку то при True отображает, что настройка включена
        self.is_hovered = False # Если курсор находится на кнопке (True), то ее нужно отрисовать подсвеченной

        self.action = action # Функция, которая должна выполняться при нажатии на кнопку

        if action is None:
            def func(): pass
            self.action = func

        if icon_name:
            self.sprite = pg.sprite.Sprite()
            self.sprite.image = load_image(icon_name)
            self.sprite.rect = self.sprite.image.get_rect()
            self.sprite.rect.topleft = self.parent.position[0] + position[0] + 4, \
                                    self.parent.position[1] + position[1] + 4
            self.parent.all_sprites.add(self.sprite)


# Класс текста для виджета
class Text:
    def __init__(self, position,
                 text = "",
                 font = None,
                 font_size = 14):
        self.position = position # Позиция текста относительно виджета

        self.font_size = font_size # Размер шрифта текста
        self.font = font # Шрифт текста
        
        self.text = text # Текст
    
    def get_font(self):
        return pg.font.Font(self.font, self.font_size)


# Класс виджета, с помощью которого можно делать меню
class Widget:
    def __init__(self, parent,
                 buttons: list[Button] = [],
                 texts: list[Text] = [],
                 button_color_1=pg.color.Color(210, 210, 210),
                 button_color_2=pg.color.Color(160, 160, 160),
                 button_color_toggled=pg.color.Color(60, 210, 210),
                 button_font_size = 36,
                 button_font = None,
                 button_border=3):
        self.parent = parent # Ссылка на класс игры, к которому прикреплен виджет

        self.position = self.top, self.left = 0, 0 # Позиция виджета на экране

        self.all_sprites = pg.sprite.Group() # Группа всех спрайтов, принадлежащих виджету

        self.buttons = buttons # Все кнопки виджета
        self.texts = texts # Все тексты виджета
        
        self.button_color_1 = button_color_1 # Цвет кнопок виджета
        self.button_color_2 = button_color_2 # Цвет рамки кнопок виджета
        self.button_color_toggled = button_color_toggled # Цвет включенной кнопки
        self.button_border = button_border # Толщина границы кнопки (визуал)
        self.button_font_size = button_font_size # Размер шрифта текста на кнопках
        self.button_font = button_font # Шрифт текста на кнопках
    
    def add_button(self, button): # Добавить кнопку в виджет
        self.buttons.append(button)
    
    def add_text(self, text): # Добавить текст в виджет
        self.texts.append(text)

    def activate_button(self, button): # Выполнить действие, присвоенное кнопке
        button.action()

    def render(self, surf): # Отрисовать виджет
        # Отрисовка текстов виджета
        for text in self.texts:
            font = text.get_font()
            txt = font.render(text.text, True, pg.color.Color(255, 255, 255))
            surf.blit(txt, (self.left + text.position[0], self.top + text.position[1]))

        # Отрисовка кнопок виджета
        for button in self.buttons:
            bc_1 = self.button_color_1
            bc_2 = self.button_color_2

            if button.is_toggled:
                bc_1 = self.button_color_toggled
                bc_2 = bc_1[0] - 50, bc_1[1] - 50, bc_1[2] - 50
            elif button.is_hovered:
                bc_1 = bc_1[0] + 30, bc_1[1] + 30, bc_1[2] + 30
                bc_2 = bc_2[0] + 20, bc_2[1] + 20, bc_2[2] + 20

            pg.draw.rect(surf, color=bc_2, rect=(
                self.left + button.position[0],
                self.top + button.position[1],
                button.size[0],
                button.size[1]))
            pg.draw.rect(surf, color=bc_1, rect=(
                self.left + button.position[0] + self.button_border,
                self.top + button.position[1] + self.button_border,
                button.size[0] - self.button_border * 2,
                button.size[1] - self.button_border * 2))
            
            font_btn_size = self.button_font_size
            font_button = pg.font.Font(self.button_font, font_btn_size)
            text_btn = font_button.render(button.text, True, (0, 0, 0))
            while text_btn.get_width() >= button.size[0] - 10: # Если текст не помещается - уменьшаем пока не вместится
                font_btn_size -= 1
                font_button = pg.font.Font(None, font_btn_size)
                text_btn = font_button.render(button.text, True, (0, 0, 0))
            surf.blit(text_btn, (self.left + button.position[0] + 5,
                                 self.top + button.position[1] + button.size[1] // 2 - 10))

        self.all_sprites.draw(surface=surf)

    def get_button(self, mouse_pos): # Получить кнопку, исходя из позиции курсора
        for button in self.buttons:
            if button.position[0] + self.left <= mouse_pos[0] <= button.position[0] + button.size[0] + self.left and \
                    button.position[1] + self.top <= mouse_pos[1] <= button.position[1] + button.size[1] + self.top:
                return button
        return None

    def get_click(self, mouse_pos): # Обработать нажатие мыши
        element = self.get_button(mouse_pos)
        if element is None:
            return
        self.activate_button(element)

    def get_motion(self, mouse_pos): # Обработать перемещение курсора
        button = self.get_button(mouse_pos)
        if button is not None and not button.is_hovered:
            for btn in self.buttons:
                btn.is_hovered = False
            button.is_hovered = True
        elif button is None:
            for btn in self.buttons:
                btn.is_hovered = False