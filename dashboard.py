"""This module provide a electric vehical dashboard dimension of 16:9 aspect ratios \
with basic features contains \n
    1) Header with date-time display and break light display. \n
    2) Speedometer with auto reset speedometer enable or disable option. \n
    3) Speedometer range adjustment from 40 upto 400. default speed range is 0 to 200. \n
    3) Battery percentage indicator. \n
    4) Charging state display. \n
    5) Accelerator state display. \n
    6) Break state display. \n
    7) Horn state display. \n
    8) Left and right indicator state display. \n
    9) You can control the above states by using several function provided in 'TriggerAction' class.\n\n
Some cool features: \n
    1) Start page with start button and creator info button. Note: you can hide creator info button
       by using hide_creator_button() method in 'TriggerAction' class. \n
    2) Loading screen launch after start button pressed. Note: you can skip loading screen 
       by using skip_loading_screen() method in 'TriggerAction' class. \n
    3) dashboard popup animation. \n
    4) you can also embed this dashboard with your own application created using PyQt by using
       'DashBoard' class.
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import random
from datetime import datetime
import sys

# painter render hints
_RENDER_HINTS = (
    QPainter.RenderHint.Antialiasing
    | QPainter.RenderHint.HighQualityAntialiasing
    | QPainter.RenderHint.SmoothPixmapTransform
    | QPainter.RenderHint.LosslessImageRendering
    | QPainter.RenderHint.Qt4CompatiblePainting
    | QPainter.RenderHint.NonCosmeticDefaultPen
    | QPainter.RenderHint.TextAntialiasing
)
_dash_board = None


class _DashBoardMain(QWidget):
    """WARNING: This is a private class. do not import this."""
    def __init__(self, parent, size: tuple | list = (1280, 720), hide_creator_button: bool = False,
        skip_start_screen: bool = False, skip_loading_screen: bool = False, do_not_move: bool = False):
        super().__init__()
        # Setting window to no icon, frameless and transparent
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAutoFillBackground(True)
        self.setFixedSize(*size)

        self.oldPos = QCursor().pos()
        self.hide_creator_button = hide_creator_button
        self.skip_start_screen = skip_start_screen
        self.skip_loading_screen = skip_loading_screen
        self.do_not_move = do_not_move

        self.initUI()

        self.keys_ = {Qt.Key.Key_W: False, Qt.Key.Key_H: False, Qt.Key.Key_Left: False, 
                        Qt.Key.Key_Right: False, Qt.Key.Key_Space: False, Qt.Key.Key_Escape: False}

        self.key_action_timer = QTimer()
        self.key_action_timer.timeout.connect(self.keyAction)
        self.key_action_timer.start(5)

    def initUI(self):
        self.stacked_widget()
        self.start_screen()
        self.loding_screen()
        self.dash_board_design()

        if self.skip_start_screen:
            self.swidget.setCurrentIndex(1)
            self.progress_bar_animation.start()

    def stacked_widget(self):
        self.swidget = QStackedWidget(self)
        self.swidget.setContentsMargins(0, 0, 0, 0)
        grad = "qlineargradient(spread:pad, x1:0.6, y1:0.4, x2:0.1, y2:0.8, stop:0 {color1}, stop:{value} {color2}, stop:1.0 {color1});".format(
            color1=QColor(0, 0, 0, 100).name(), color2=QColor(13, 13, 13).name(), value=0.5)
        self.setStyleSheet("background-color: %s;"%grad)
        self.swidget.setFixedSize(self.width(), self.height())

    def start_screen(self):
        start_up_widget = QWidget()
        start_up_widget.setFixedSize(self.width(), self.height())
        self.swidget.addWidget(start_up_widget)

        start_button = QPushButton("Start", start_up_widget)
        start_button.setFixedSize(self.width()//5, self.width()//5)
        start_button.move(self.rect().center()-start_button.rect().center())

        grad = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=QColor(240, 0, 0).name(), color2=QColor(255, 80, 0).name(), value=0.5)
        hover_grad = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=QColor(0, 240, 0).name(), color2=QColor(80, 255, 0).name(), value=0.5)
        start_button_style = """QPushButton {background-color: %s; color: white; border-radius: %spx}
                                QPushButton::hover {background-color: %s;}"""% (grad, str(self.width()//10), hover_grad)
        start_button.setStyleSheet(start_button_style)

        start_button_shadow = QGraphicsDropShadowEffect()
        start_button_shadow.setBlurRadius(15)
        start_button.setGraphicsEffect(start_button_shadow)

        start_button_font = QFont("Consolas", 0, 0, True)
        start_button_font.setBold(True)
        start_button_font.setPixelSize(round(self.width()*0.05))
        start_button.setFont(start_button_font)

        start_button.clicked.connect(self.start_button_action)
        
        creator_info_button = QPushButton("C", start_up_widget)
        creator_info_button.setContentsMargins(0, 0, 80, 0)
        creator_info_button.setFixedSize(*map(round, (self.width()*0.05, self.width()*0.05)))
        creator_info_button.move(self.rect().bottomRight()-creator_info_button.rect().bottomRight()-creator_info_button.rect().center())
        
        creator_info_font = QFont("Arial Black", 0, 0, True)
        creator_info_font.setBold(True)
        creator_info_font.setPixelSize(round(self.width()*0.03))
        creator_info_button.setFont(creator_info_font)

        creator_info_button_style = """QPushButton {background-color: rgba(0, 0, 0, 0); color: rgb(153, 153, 0); border-radius: %spx;}
                                QPushButton::hover {color: rgb(255, 255, 0);}"""% str(round(creator_info_button.width()*0.5))
        creator_info_button.setStyleSheet(creator_info_button_style)
        creator_info_button.clicked.connect(self.creator_info_button_action)

        creator_info_label = QLabel(start_up_widget)
        creator_info_label.setContentsMargins(0, 0, 0, 0)
        creator_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        creator_info_label.setFixedSize(*map(round, (self.width()*0.6, self.height()*0.1)))
        creator_info_label.move(self.rect().center()-creator_info_label.rect().center()-QPoint(-round(self.width()*0.8), round(-self.height()//2+creator_info_label.height()*0.9)))
        
        grad = "qlineargradient(spread:pad, x1:0.5, y1:0.7, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color2});".format(
            color1=QColor(255, 153, 51).name(), color2=QColor(77, 77, 0).name(), value=0.5)
        creator_info_label.setStyleSheet("background-color: %s; color: rgb(204, 255, 255)"% grad)

        creator_info_font.setPixelSize(round(self.width()*0.015))
        creator_info_label.setFont(creator_info_font)
        creator_info_label.setWordWrap(True)
        creator_info_label.setOpenExternalLinks(True)
        creator_info_label.setText('<font color=FloralWhite>Creator info:</font> <br> <font color=Ivory>Name:</font> Prasanna K; <font color=Ivory>GitHub link:</font> <a href="https://github.com/prasanna892"><font color=white>https://github.com/prasanna892.</font></a>')

        creator_info_button.setHidden(self.hide_creator_button)

        self.creator_label_ani = QPropertyAnimation(creator_info_label, b"pos")
        self.creator_label_ani.setStartValue(creator_info_label.pos())
        self.creator_label_ani.setEndValue(QPoint(round(self.height()*0.55), creator_info_label.y()))
        self.creator_label_ani.setDuration(600)
        self.creator_label_ani.setDirection(1)

    def creator_info_button_action(self):
        self.creator_label_ani.setDirection(not self.creator_label_ani.direction())
        self.creator_label_ani.start()

    def start_button_action(self):
        if self.skip_loading_screen: 
            self.swidget.setCurrentIndex(2)
            self.dash_board_design_widget.start_up_animation()
        else:
            self.swidget.setCurrentIndex(1)
            self.progress_bar_animation.start()

    def loding_screen(self):
        loading_screen_widget = QWidget()
        loading_screen_widget.setContentsMargins(0, 0, 0, 0)
        loading_screen_widget.setFixedSize(self.width(), self.height())
        self.swidget.addWidget(loading_screen_widget)

        get_ready_label = QLabel(loading_screen_widget)
        get_ready_label.setFixedSize(*map(round, (self.width()*0.6, self.height()*0.2)))
        get_ready_label.move(self.rect().center()-get_ready_label.rect().center()-QPoint(0, get_ready_label.height()))
        get_ready_label.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: rgb(207, 184, 29)")
        get_ready_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        saftey_rule_font = QFont("Consolas", 0, 0, True)
        saftey_rule_font.setBold(True)
        saftey_rule_font.setPixelSize(round(self.width()*0.035))
        get_ready_label.setFont(saftey_rule_font)
        get_ready_label.setText("Get ready for the ride...")

        loding_progress_bar = QProgressBar(loading_screen_widget)
        loding_progress_bar.setContentsMargins(0, 0, 0, 0)
        loding_progress_bar.setFixedSize(*map(round, (loading_screen_widget.width()*0.7, loading_screen_widget.height()*0.1)))
        loding_progress_bar.move(self.rect().center()-loding_progress_bar.rect().center())
        loding_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        loding_progress_bar_font = QFont("Consolas", 0, 0, True)
        loding_progress_bar_font.setBold(True)
        loding_progress_bar_font.setPixelSize(round(self.width()*0.04))
        loding_progress_bar.setFont(loding_progress_bar_font)

        grad = "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color3});".format(
            color1=QColor(240, 0, 0).name(), color2=QColor(255, 80, 0).name(), color3=QColor(255, 255, 0).name(), value=0.3)
        loding_progress_bar.setStyleSheet("QProgressBar {background-color: rgba(0, 0, 0, 0); color: white; border-radius: %spx;}"%str(loding_progress_bar.height()//2)
            + "QProgressBar::chunk {background-color: %s; border-radius: %spx;}"%(grad, str(loding_progress_bar.height()//2)))

        self.progress_bar_animation = QPropertyAnimation(loding_progress_bar, b"value")
        self.progress_bar_animation.setStartValue(loding_progress_bar.height()*0.2)
        self.progress_bar_animation.valueChanged.connect(self.driving_rule_info)
        self.progress_bar_animation.setEndValue(100)
        self.progress_bar_animation.setDuration(3000)

        self.saftey_rules = ("Do not drink and drive.", "Always wear a helmet!", "Drive within the speed limits.", 
                            "Don't use mobile phones while driving.", "Buckle up before you drive.", "Keep a safe distance from vehicles!")

        self.saftey_rule_label = QLabel(loading_screen_widget)
        self.saftey_rule_label.setFixedSize(*map(round, (self.width()*0.6, self.height()*0.2)))
        self.saftey_rule_label.move(self.rect().center()-self.saftey_rule_label.rect().center()+QPoint(0, self.saftey_rule_label.height()))
        self.saftey_rule_label.setStyleSheet("background-color: rgba(0, 0, 0, 0); color: yellow")
        self.saftey_rule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        saftey_rule_font = QFont("Consolas", 0, 0, True)
        saftey_rule_font.setBold(True)
        saftey_rule_font.setPixelSize(round(self.width()*0.025))
        self.saftey_rule_label.setFont(saftey_rule_font)
        self.saftey_rule_label.setText(random.sample(self.saftey_rules, 1)[0])

    def driving_rule_info(self, val):
        if val%33==0 and val!=99:
            self.saftey_rule_label.setText(random.sample(self.saftey_rules, 1)[0])
        if val==100:
            self.swidget.setCurrentIndex(2)
            self.dash_board_design_widget.start_up_animation()

    def dash_board_design(self):
        self.dash_board_design_widget = _DashBoardContolsDesign(self.swidget)
        self.swidget.addWidget(self.dash_board_design_widget)

    def mouseDoubleClickEvent(self, event):
        pass

    def mousePressEvent(self, event):
        if not self.do_not_move: self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if not self.do_not_move:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            QCoreApplication.instance().quit()

    def customKeyPressEvent(self, event):
        # indicator
        if event.key() == Qt.Key.Key_Left:
            self.keys_[event.key()] = True
            self.dash_board_design_widget.indicator_triger(0)
        if event.key() == Qt.Key.Key_Right:
            self.keys_[event.key()] = True
            self.dash_board_design_widget.indicator_triger(1)
        
        # horn
        if event.key() == Qt.Key.Key_H or self.keys_[Qt.Key.Key_H]:
            self.keys_[event.key()] = True

        # speedometer
        if event.key() == Qt.Key.Key_W or self.keys_[Qt.Key.Key_W]:
            self.keys_[event.key()] = True

        # break
        if event.key() == Qt.Key.Key_Space or self.keys_[Qt.Key.Key_Space]:
            self.keys_[event.key()] = True
    
    def customKeyReleaseEvent(self, event):
        # indicator
        if event.key() == Qt.Key.Key_Left and not event.isAutoRepeat():
            self.keys_[event.key()] = False
        if event.key() == Qt.Key.Key_Right and not event.isAutoRepeat():
            self.keys_[event.key()] = False
        
        # speedometer
        if event.key() == Qt.Key.Key_W and not event.isAutoRepeat():
            self.keys_[event.key()] = False
            self.dash_board_design_widget.set_accelerator_state(0)

        # horn
        if event.key() == Qt.Key.Key_H and not event.isAutoRepeat():
            self.keys_[event.key()] = False
            self.dash_board_design_widget.set_horn_state(0)

        # break
        if event.key() == Qt.Key.Key_Space and not event.isAutoRepeat():
            self.keys_[event.key()] = False
            self.dash_board_design_widget.set_break_state(0)

    def keyAction(self):
        if any(self.keys_.values()):
            # horn
            if self.keys_[Qt.Key.Key_H]:
                self.dash_board_design_widget.set_horn_state(1)

            # speedometer
            if self.keys_[Qt.Key.Key_W]:
                self.dash_board_design_widget.set_accelerator_state(1)

            # break
            if self.keys_[Qt.Key.Key_Space]:
                self.dash_board_design_widget.set_break_state(1)
   
    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.KeyPress:
            self.customKeyPressEvent(event)
        if event.type() == QEvent.Type.KeyRelease:
            if not event.isAutoRepeat():
                self.customKeyReleaseEvent(event)

        return super().eventFilter(source, event)


class _DashBoardContolsDesign(QWidget):
    """WARNING: This is a private class. do not import this."""
    def __init__(self, parent=None):
        super(_DashBoardContolsDesign, self).__init__(parent)
        self.parent_ = parent
        self.resize(self.parent_.size())
        self.setContentsMargins(0, 0, 0, 0)

        self.header_properties()
        self.indicators_properties()
        self.horn_properties()
        self.charge_properties()
        self.break_properties()
        self.accelerator_properties()
        self.speedometer_properties()
        self.battery_properties()

    def header_properties(self):
        self.header_border_color_lst = (QColorConstants.Svg.orchid, QColorConstants.Svg.red)
        self.header_border_color = 0

        self.show_time = 0
        self.time_update_timer = QTimer()
        self.time_update_timer.timeout.connect(lambda: self.repaint())
        self.time_update_timer.start(1000)

        # drawing boarder
        header_trans = QTransform()
        header_trans.scale(self.width()*0.012, self.height()*0.008)
        header_boarder = QPolygonF((QPointF(10, 10), QPointF(15, 10), QPointF(25, 25), 
                                QPointF(55, 25), QPointF(65, 10), QPointF(70, 10),
                                QPointF(60, 30), QPointF(20, 30)))
        self.scaled_header_border = header_trans.map(header_boarder)
        scaled_header_border_bounding_rect = QRect(self.scaled_header_border.boundingRect().toRect())
        self.scaled_header_border.translate(self.rect().center()-scaled_header_border_bounding_rect.center())
        self.scaled_header_border.translate(0, -self.rect().height()*0.5+scaled_header_border_bounding_rect.height()*0.5)

        # drawing inner
        header_inner = QPolygonF((QPointF(15, 10), QPointF(25, 25),
                                QPointF(55, 25), QPointF(65, 10)))
        self.scaled_header_inner = header_trans.map(header_inner)
        scaled_header_inner_bounding_rect = QRect(self.scaled_header_inner.boundingRect().toRect())
        self.scaled_header_inner.translate(self.rect().center()-scaled_header_inner_bounding_rect.center())
        self.scaled_header_inner.translate(0, -self.rect().height()*0.5+scaled_header_inner_bounding_rect.height()*0.5)

    def header_painting(self, painter: QPainter):
        # drawing boarder
        painter.setPen(QPen(QGradient(QGradient.Preset.Blessing), round(self.width()*0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.setBrush(QBrush(self.header_border_color_lst[self.header_border_color], Qt.BrushStyle.Dense4Pattern))
        painter.drawPolygon(self.scaled_header_border)

        # drawing inner
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(76, 97, 78, 100)))
        painter.drawPolygon(self.scaled_header_inner)

        painter.setPen(QPen(QGradient(QGradient.Preset.Blessing), round(self.width()*0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.drawPolygon(self.scaled_header_border)

        # drawing time
        now = datetime.now()

        time_font = QFont("Consolas", 0, 0, True)
        time_font.setPixelSize(round(self.width()*0.04))
        time_fm = QFontMetrics(time_font)
        time_rect = time_fm.boundingRect(now.strftime("%I:%M:%S%p %d %a"))
        painter.setFont(time_font)

        scaled_header_inner_bounding_rect = self.scaled_header_inner.boundingRect().toRect()
        time_rect.moveCenter(scaled_header_inner_bounding_rect.center())

        painter.setPen(QPen(QGradient(QGradient.Preset.FreshOasis), round(self.width()*0.0012)))
        if self.show_time: painter.drawText(time_rect, Qt.AlignmentFlag.AlignCenter, now.strftime("%I:%M:%S%p %a %d"))

    def indicators_properties(self):
        self.indicator_timer = QTimer()
        self.indicator_timer.timeout.connect(self.indicator_blink_animation)

        self.indicator_color_list = (QColorConstants.DarkGreen, QColorConstants.Green)

        self.right_indicator_color = self.indicator_color_list[0]
        self.left_indicator_color = self.indicator_color_list[0]

        self.right_indicator_state = 0
        self.left_indicator_state = 0

        self.right_indicator_blink = 0
        self.left_indicator_blink = 0

        # left indicator
        indicator_trans = QTransform()
        indicator_trans.scale(self.width()*0.001, self.height()*0.0015)
        left_idicator = QPolygonF((QPointF(40, 80), QPointF(90, 120), QPointF(90, 100), QPointF(150, 100),
                                    QPointF(150, 60), QPointF(90, 60), QPointF(90, 40)))
        self.scaled_left_idicator = indicator_trans.map(left_idicator)
        self.scaled_left_idicator.translate(-self.scaled_left_idicator.boundingRect().x(), -self.scaled_left_idicator.boundingRect().y())
        self.scaled_left_idicator.translate(self.width()*0.03, self.height()*0.06)

        # right indicator
        rotate_t = QTransform()
        rotate_t.rotate(180, Qt.Axis.YAxis)
        self.scaled_right_idicator = self.scaled_left_idicator
        self.scaled_right_idicator = rotate_t.map(self.scaled_right_idicator)
        self.scaled_right_idicator.translate(-self.scaled_right_idicator.boundingRect().x(), -self.scaled_right_idicator.boundingRect().y())
        self.scaled_right_idicator.translate(self.width()-self.scaled_right_idicator.boundingRect().width()-self.scaled_left_idicator.boundingRect().x(), self.height()*0.06)

    def indicators_painting(self, painter: QPainter):
        # drawing left indicator
        painter.setPen(QPen(self.left_indicator_color, round(self.width()*0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.setBrush(QBrush(self.left_indicator_color, Qt.BrushStyle.Dense3Pattern))
        painter.drawPolygon(self.scaled_left_idicator)
        
        # drawing right indicator
        painter.setPen(QPen(self.right_indicator_color, round(self.width()*0.0012), join=Qt.PenJoinStyle.MiterJoin))
        painter.setBrush(QBrush(self.right_indicator_color, Qt.BrushStyle.Dense3Pattern))
        painter.drawPolygon(self.scaled_right_idicator)

    def indicator_triger(self, indecator):
        if indecator==0: # left indicator
            self.left_indicator_state = not self.left_indicator_state
        if indecator==1: # right indicator
            self.right_indicator_state = not self.right_indicator_state

        if self.right_indicator_state or self.left_indicator_state:
            self.indicator_timer.start(600) # blink indicator interval of 600ms
        else:
            self.indicator_blink_animation()
            self.indicator_timer.stop()
            
    def indicator_blink_animation(self):
        if self.right_indicator_state:
            self.right_indicator_color = self.indicator_color_list[self.right_indicator_blink]
            self.right_indicator_blink = not self.right_indicator_blink
        else:
            self.right_indicator_color = self.indicator_color_list[0]

        if self.left_indicator_state:
            self.left_indicator_color = self.indicator_color_list[self.left_indicator_blink]
            self.left_indicator_blink = not self.left_indicator_blink
        else:
            self.left_indicator_color = self.indicator_color_list[0]

        self.repaint()

    def horn_properties(self):
        self.horn_sound_color_lst = (QColor(67, 13, 13, 200), QGradient(QGradient.Preset.BlackSea))
        self.horn_sound_color_idx = 0
        self.horn_state = 0 # 0 -> off 1 -> on

    def horn_painting(self, painter: QPainter):
        painter.setPen(QPen(QColorConstants.Black, round(self.width()*0.0012)))
        painter.setBrush(QBrush(QGradient(QGradient.Preset.RichMetal)))

        horn_trans = QTransform()
        horn_trans.scale(self.width()*0.0012, self.height()*0.002)

        horn = QPolygonF((QPointF(40, 50), QPointF(60, 50), QPointF(90, 30), QPointF(100, 30),
                        QPointF(100, 100), QPointF(90, 100), QPointF(60, 80), QPointF(40, 80)))

        scaled_horn = horn_trans.map(horn)
        scaled_horn.translate(-scaled_horn.boundingRect().x(), -scaled_horn.boundingRect().y())
        scaled_horn.translate(self.width()*0.03, self.height()*0.7)
        painter.drawPolygon(scaled_horn)

        horn_rect = scaled_horn.boundingRect().toRect()

        painter.setPen(QPen(QColorConstants.Gray, round(self.width()*0.0012)))
        painter.drawLine(horn_rect.topRight(), horn_rect.bottomRight())

        painter.setPen(QPen(self.horn_sound_color_lst[self.horn_sound_color_idx], round(self.width()*0.0025), cap=Qt.PenCapStyle.RoundCap))

        sound_rect1 = QRect(0, 0, round(horn_rect.width()*1.5), round(horn_rect.height()*1.5))
        sound_rect1.moveCenter(horn_rect.center())
        sound_rect1.moveRight(round(horn_rect.width()*1.7))
        painter.drawArc(sound_rect1.x(), sound_rect1.y(), sound_rect1.width(), sound_rect1.height(), 35*16, -70*16)
        
        sound_rect2 = QRect(0, 0, round(horn_rect.width()*1.3), round(horn_rect.height()*1.3))
        sound_rect2.moveCenter(horn_rect.center())
        sound_rect2.moveRight(round(horn_rect.width()*1.6))
        painter.drawArc(sound_rect2.x(), sound_rect2.y(), sound_rect2.width(), sound_rect2.height(), 27*16, -55*16)

        sound_rect3 = QRect(0, 0, round(horn_rect.width()*1.2), round(horn_rect.height()*1.2))
        sound_rect3.moveCenter(horn_rect.center())
        sound_rect3.moveRight(round(horn_rect.width()*1.5))
        painter.drawArc(sound_rect3.x(), sound_rect3.y(), sound_rect3.width(), sound_rect3.height(), 17*16, -35*16)

    def set_horn_state(self, val):
        self.horn_sound_color_idx = val
        if self.horn_sound_color_idx != self.horn_state:
            self.repaint()
        self.horn_state = val

    def charge_properties(self):
        self.charge_default_state = 0
        self.charge_state = 0
        self.charge_color_lst = (QColor(67, 13, 13, 200), QGradient(QGradient.Preset.HeavyRain))

    def set_charge_state(self, val):
        self.charge_default_state = val
        self.charge_state = val
        self.repaint()

    def charge_painting(self, painter: QPainter):
        # setting charge font
        charge_font = QFont("Consolas", 0, 0, True)
        charge_font.setPixelSize(round(self.width()*0.031))
        charge_fm = QFontMetrics(charge_font)
        charge_rect = charge_fm.boundingRect("CHARGING")
        painter.setFont(charge_font)

        charge_rect.moveTo(self.rect().center()+QPointF(self.rect().width()*0.328, -self.rect().height()*0.07).toPoint())

        painter.setPen(QPen(self.charge_color_lst[self.charge_state], round(self.width()*0.0025)))
        painter.drawText(charge_rect, Qt.AlignmentFlag.AlignCenter, "CHARGING")

    def break_properties(self):
        self.break_state = 0
        self.break_color_lst = (QColor(67, 13, 13, 200), QGradient(QGradient.Preset.ColorfulPeach))

    def set_break_state(self, val):
        self.break_state = val
        self.header_border_color = val
        self.repaint()

    def break_painting(self, painter: QPainter):
        # setting break font
        break_font = QFont("Consolas", 0, 0, True)
        break_font.setPixelSize(round(self.width()*0.045))
        break_fm = QFontMetrics(break_font)
        break_rect = break_fm.boundingRect("BREAK")
        painter.setFont(break_font)

        break_rect.moveTo(self.rect().center()+QPointF(self.rect().width()*0.345, self.rect().height()*0.1).toPoint())

        painter.setPen(QPen(self.break_color_lst[self.break_state], round(self.width()*0.0025)))
        painter.drawText(break_rect, Qt.AlignmentFlag.AlignCenter, "BREAK")

    def accelerator_properties(self):
        self.speed_angle_factor = 200/300  # 200 default top speed and 300 available angle of speedometer
        self.speed = 0
        self.accelerator_state = 0
        self.accelerator_color_lst = (QColor(67, 13, 13, 200), QGradient(QGradient.Preset.FruitBlend))

    def set_speed(self, val):
        self.speed = round(val/self.speed_angle_factor) if round(val/self.speed_angle_factor)<=300 else 300
        self.repaint()

    def get_speed(self):
        return round(self.speed*self.speed_angle_factor)

    def set_accelerator_state(self, val):
        self.accelerator_state = val
        if self.speed <= 300 and not self.break_state:
            self.speed += self.speed_angle_factor
            self.repaint()
    
    def accelerator_painting(self, painter: QPainter):
        # setting accelerator font
        accelerator_font = QFont("Consolas", 0, 0, True)
        accelerator_font.setPixelSize(round(self.width()*0.031))
        accelerator_fm = QFontMetrics(accelerator_font)
        accelerator_rect = accelerator_fm.boundingRect("ACCELERATE")
        painter.setFont(accelerator_font)

        accelerator_rect.moveTo(self.rect().center()+QPointF(self.rect().width()*0.3, self.rect().height()*0.3).toPoint())

        painter.setPen(QPen(self.accelerator_color_lst[self.accelerator_state], round(self.width()*0.0025)))
        painter.drawText(accelerator_rect, Qt.AlignmentFlag.AlignCenter, "ACCELERATE")

    def speedometer_properties(self):
        self.speedometer_bounding_rect = QRectF(self.width()*0.173, self.height()*1.01, self.width()*0.4, self.width()*0.4)
        
        self.enable_speedometer_resetter = True

        self.speedometer_resetter_timer = QTimer()
        self.speedometer_resetter_timer.timeout.connect(self.speedometer_resetter)
        self.speedometer_resetter_timer.start(5)

        self.speed_range = 200
        self.for_loop_count = self.speed_range//20 + 2
        self.angle_to_rotate = 300/(self.speed_range/20)
        self.compromise_angle = 30-self.angle_to_rotate
        self.compromise_angle_half = self.compromise_angle+self.angle_to_rotate/2
        self.enable_sub_number = True

    def set_speedometer_range(self, top_speed):
        if 40 <= top_speed <= 400:
            self.speed_range = int(top_speed-top_speed%-20 if top_speed%20>=10 else top_speed-top_speed%20)
        elif top_speed < 40: self.speed_range = 40
        elif top_speed > 400: self.speed_range = 400

        self.speed_angle_factor = self.speed_range/300
        self.for_loop_count = self.speed_range//20 + 2
        self.angle_to_rotate = 300/(self.speed_range/20)
        self.compromise_angle = 30-self.angle_to_rotate
        self.compromise_angle_half = self.compromise_angle+self.angle_to_rotate/2
        self.enable_sub_number = True if self.speed_range<=260 else False
        self.repaint()

    def set_speedometer_resetter_state(self, val):
        self.enable_speedometer_resetter = val

    def speedometer_resetter(self):
        if self.speed>0 and self.enable_speedometer_resetter:
            if not self.accelerator_state: # accelerator released
                if self.break_state: # break presssed
                    self.speed -= 3*self.speed_angle_factor
                else: 
                    self.speed -= self.speed_angle_factor
            if self.break_state: # break presssed
                self.speed -= 2*self.speed_angle_factor
            if self.speed<0: self.speed = 0
            self.repaint()

    def speedometer_painting(self, painter: QPainter):
        # inner dial design
        conicalGradient = QConicalGradient(QPointF(self.speedometer_bounding_rect.width()/2, self.speedometer_bounding_rect.width()/2), -59*16)
        conicalGradient.setColorAt(0.2, QColorConstants.Green)
        conicalGradient.setColorAt(0.7, QColorConstants.Yellow)
        conicalGradient.setColorAt(0.5, QColorConstants.Red)
        inner_dial = self.speedometer_bounding_rect.toRect()
        inner_dial.setSize(QSizeF(self.speedometer_bounding_rect.width()*0.975, self.speedometer_bounding_rect.width()*0.975).toSize())
        inner_dial.moveCenter(self.speedometer_bounding_rect.center().toPoint())
        painter.setPen(QPen(conicalGradient, self.width()*0.01))
        painter.drawArc(inner_dial, -59*16, 298*16)

        # setting number font
        number_font = QFont("Consolas", 0, 0, True)
        number_font.setPixelSize(round(self.width()*0.02))
        number_fm = QFontMetrics(number_font)
        number_rect = number_fm.boundingRect("000")
        painter.setFont(number_font)

        # drawing main number and spike
        painter.setPen(QPen(QGradient(QGradient.Preset.FebruaryInk), self.width()*0.005))
        center = self.speedometer_bounding_rect.center()
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(self.compromise_angle)
        painter.translate(-center.x(), -center.y())
        for a in range(1, self.for_loop_count):
            painter.translate(center.x(), center.y())
            painter.rotate(self.angle_to_rotate)
            painter.translate(-center.x(), -center.y())
            # spike
            spike_p1 = center+QPointF(0, self.speedometer_bounding_rect.height()//2)
            spike_p2 = center+QPointF(0, self.speedometer_bounding_rect.height()*0.45)
            painter.drawLine(spike_p1, spike_p2)
            # number
            number_point = spike_p2.toPoint()-QPoint(0, round(self.width()*0.02))
            painter.save()
            painter.translate(number_point.x(), number_point.y())
            painter.rotate(a*-self.angle_to_rotate-self.compromise_angle)
            painter.translate(-number_point.x(), -number_point.y())
            number_rect.moveCenter(number_point)
            painter.drawText(number_rect, Qt.AlignmentFlag.AlignCenter, str((a-1)*20))
            painter.restore()
        painter.restore()

        # drawing sub number and spike
        painter.setPen(QPen(QGradient(QGradient.Preset.FebruaryInk), self.width()*0.003))
        number_font.setPixelSize(round(self.width()*0.015))
        painter.setFont(number_font)
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(self.compromise_angle_half)
        painter.translate(-center.x(), -center.y())
        for a in range(1, self.for_loop_count-1):
            painter.translate(center.x(), center.y())
            painter.rotate(self.angle_to_rotate)
            painter.translate(-center.x(), -center.y())
            # spike
            spike_p1 = center+QPointF(0, self.speedometer_bounding_rect.height()//2)
            spike_p2 = center+QPointF(0, self.speedometer_bounding_rect.height()*0.47)
            painter.drawLine(spike_p1, spike_p2)
            # number
            number_point = spike_p2.toPoint()-QPoint(0, round(self.width()*0.02))
            if self.enable_sub_number:
                painter.save()
                painter.translate(number_point.x(), number_point.y())
                painter.rotate(a*-self.angle_to_rotate-self.compromise_angle_half)
                painter.translate(-number_point.x(), -number_point.y())
                number_rect.moveCenter(number_point)
                painter.drawText(number_rect, Qt.AlignmentFlag.AlignCenter, str((2*a-1)*10))
                painter.restore()
        painter.restore()

        # drawing hand
        painter.setPen(QPen(QGradient(QGradient.Preset.Blessing), round(self.width()*0.003), cap=Qt.PenCapStyle.RoundCap))
        painter.setBrush(QBrush(QGradient(QGradient.Preset.Blessing)))
        hand_polygon = (center + QPoint(0, round(self.height()*0.0055)), center + QPoint(0, -round(self.height()*0.0055)), center + QPoint(round(self.height()*0.28), 0))
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(120+self.speed)
        painter.translate(-center.x(), -center.y())
        painter.drawPolygon(hand_polygon)
        painter.restore()

        # drawing center point
        painter.setPen(QPen(QGradient(QGradient.Preset.CrystalRiver), round(self.width()*0.03), cap=Qt.PenCapStyle.RoundCap))
        painter.drawPoint(center)

        # drawing outer dial
        painter.setPen(QPen(QGradient(QGradient.Preset.CrystalRiver), self.width()*0.005))
        painter.drawArc(self.speedometer_bounding_rect.toRect(), -60*16, 300*16)

        # drawing speed in word
        painter.setPen(QPen(QGradient(QGradient.Preset.Crystalline), self.width()*0.005))
        speed_font = QFont("Consolas", 0, 0, True)
        speed_font.setPixelSize(round(self.width()*0.035))
        speed_fm = QFontMetrics(speed_font)
        # speed hm/h
        speed_kmph_rect = speed_fm.boundingRect("000-km/h")
        painter.setFont(speed_font)
        speed_kmph_rect.moveCenter(center.toPoint())
        speed_kmph_rect.moveBottom(round(self.speedometer_bounding_rect.bottom()))
        painter.drawText(speed_kmph_rect, Qt.AlignmentFlag.AlignCenter, f'{self.get_speed()} km/h')
        # speed
        speed_word_rect = speed_fm.boundingRect("SPEED")
        painter.setFont(speed_font)
        speed_word_rect.moveCenter(center.toPoint())
        speed_word_rect.moveBottom(round(self.speedometer_bounding_rect.bottom()-speed_kmph_rect.height()))
        painter.drawText(speed_word_rect, Qt.AlignmentFlag.AlignCenter, "SPEED")

    def battery_properties(self):
        self.set_battery(100)

    def set_battery(self, val):
        self.battery = 100-round(val/0.555) if round(val/0.555)<=180 else 180
        self.repaint()

    def get_battery(self):
        return 56-round(self.battery*0.555)

    def battery_indicator_painting(self, painter):
        battery_bounding_rect = self.speedometer_bounding_rect.toRect()
        battery_bounding_rect.setSize(QSizeF(battery_bounding_rect.width()*0.8, battery_bounding_rect.width()*0.8).toSize())
        battery_bounding_rect.moveBottomLeft(self.speedometer_bounding_rect.toRect().bottomRight()-QPoint(round(battery_bounding_rect.width()*0.2), 0))

        # inner dial
        inner_dial = QRect(*battery_bounding_rect.getRect())
        inner_dial.setSize(QSizeF(battery_bounding_rect.width()*0.975, battery_bounding_rect.width()*0.975).toSize())
        inner_dial.moveCenter(battery_bounding_rect.center())
        painter.setPen(QPen(QColorConstants.Svg.red, self.width()*0.01))
        painter.drawArc(inner_dial, -22*16, -34*16)
        painter.setPen(QPen(QColor(224, 210, 13, 210), self.width()*0.01))
        painter.drawArc(inner_dial, 14*16, -34*16)
        painter.setPen(QPen(QColor(66, 245, 66, 190), self.width()*0.01))
        painter.drawArc(inner_dial, 121*16, -104*16)

        # setting number font
        number_font = QFont("Consolas", 0, 0, True)
        number_font.setPixelSize(round(self.width()*0.02))
        number_fm = QFontMetrics(number_font)
        number_rect = number_fm.boundingRect("000")
        painter.setFont(number_font)

        # drawing main number and spike
        painter.setPen(QPen(QGradient(QGradient.Preset.FebruaryInk), self.width()*0.005))
        center = battery_bounding_rect.center()
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(129)
        painter.translate(-center.x(), -center.y())
        for a in range(1, 12):
            painter.translate(center.x(), center.y())
            painter.rotate(18)
            painter.translate(-center.x(), -center.y())
            # spike
            spike_p1 = center+QPointF(0, battery_bounding_rect.height()*0.495)
            spike_p2 = center+QPointF(0, battery_bounding_rect.height()*0.45)
            painter.drawLine(spike_p1, spike_p2)
            # number
            number_point = spike_p2.toPoint()-QPoint(0, round(self.width()*0.02))
            painter.save()
            painter.translate(number_point.x(), number_point.y())
            painter.rotate(a*-18-129)
            painter.translate(-number_point.x(), -number_point.y())
            number_rect.moveCenter(number_point)
            painter.drawText(number_rect, Qt.AlignmentFlag.AlignCenter, str(100-(a-1)*10))
            painter.restore()
        painter.restore()

        # drawing hand
        painter.setPen(QPen(QGradient(QGradient.Preset.AmyCrisp), round(self.width()*0.003), cap=Qt.PenCapStyle.RoundCap, join=Qt.PenJoinStyle.RoundJoin))
        painter.setBrush(QBrush(QGradient(QGradient.Preset.AmyCrisp)))
        hand_polygon = (center+QPoint(0, round(self.height()*0.0045)), center+QPoint(0, -round(self.height()*0.0045)), center+QPoint(round(self.height()*0.22), 0))
        painter.save()
        painter.translate(center.x(), center.y())
        painter.rotate(-43+self.battery)
        painter.translate(-center.x(), -center.y())
        painter.drawPolygon(hand_polygon)
        painter.restore()

        # drawing center point
        painter.setPen(QPen(QColorConstants.Svg.lemonchiffon, round(self.width()*0.02), cap=Qt.PenCapStyle.RoundCap))
        painter.drawPoint(center)
        
        # drawing outer dial
        painter.setPen(QPen(QColorConstants.Svg.lemonchiffon, self.width()*0.005))
        painter.drawArc(battery_bounding_rect, 303*16, 190*16)

        # once again drawing outer dial of speedometer to hide overlap
        painter.setPen(QPen(QGradient(QGradient.Preset.CrystalRiver), self.width()*0.005))
        painter.drawArc(self.speedometer_bounding_rect.toRect(), -60*16, 300*16)

        # drawing battery percent in word
        painter.setPen(QPen(QGradient(QGradient.Preset.CrystalRiver), self.width()*0.005))
        battery_font = QFont("Consolas", 0, 0, True)
        battery_font.setPixelSize(round(self.width()*0.035))
        battery_fm = QFontMetrics(battery_font)
        # battery percent
        battery_percent_rect = battery_fm.boundingRect("000%")
        painter.setFont(battery_font)
        battery_percent_rect.moveCenter(center)
        battery_percent_rect.moveBottom(battery_bounding_rect.bottom())
        battery_percent_rect.moveLeft(round(battery_bounding_rect.x()+battery_bounding_rect.width()*0.23))
        painter.drawText(battery_percent_rect, Qt.AlignmentFlag.AlignCenter, f'{self.get_battery()}%')
        # battery
        battery_word_rect = battery_fm.boundingRect("BATTERY")
        painter.setFont(battery_font)
        battery_word_rect.moveCenter(center)
        battery_word_rect.moveBottom(battery_bounding_rect.bottom()-battery_percent_rect.height())
        battery_word_rect.moveLeft(round(battery_bounding_rect.x()+battery_bounding_rect.width()*0.15))
        painter.drawText(battery_word_rect, Qt.AlignmentFlag.AlignCenter, "BATTERY")

    def start_up_animation(self):
        self.other_visible = False

        indicator_animation = QVariantAnimation(self)
        indicator_animation.setStartValue(self.width())
        indicator_animation.setEndValue(round(self.width()*0.03))
        indicator_animation.valueChanged.connect(self.indicator_animation)
        indicator_animation.setDuration(500)

        header_animation = QVariantAnimation(self)
        header_animation.setStartValue(0)
        header_animation.setEndValue(round(self.scaled_header_border.boundingRect().height()))
        header_animation.valueChanged.connect(self.header_animation)
        header_animation.setDuration(300)

        speedometer_popup_animation = QVariantAnimation(self)
        speedometer_popup_animation.setStartValue(round(self.height()*1.01))
        speedometer_popup_animation.setEndValue(round(self.height()*0.2))
        speedometer_popup_animation.valueChanged.connect(self.speedometer_popup_animation)
        speedometer_popup_animation.finished.connect(self.other_popup_animation)
        speedometer_popup_animation.setDuration(500)

        speedometer_animation1 = QVariantAnimation(self)
        speedometer_animation1.setStartValue(0)
        speedometer_animation1.setEndValue(300)
        speedometer_animation1.valueChanged.connect(self.speedometer_animation)
        speedometer_animation1.setDuration(1000)

        speedometer_animation2 = QVariantAnimation(self)
        speedometer_animation2.setStartValue(300)
        speedometer_animation2.setEndValue(0)
        speedometer_animation2.valueChanged.connect(self.speedometer_animation)
        speedometer_animation2.setDuration(1000)

        check_all_state_animation = QVariantAnimation(self)
        check_all_state_animation.currentLoopChanged.connect(self.check_all_state_animation)
        check_all_state_animation.setDuration(200)
        check_all_state_animation.setLoopCount(10)

        sa_speeddial_group = QSequentialAnimationGroup(self)
        sa_speeddial_group.addAnimation(speedometer_animation1)
        sa_speeddial_group.insertPause(1, 50)
        sa_speeddial_group.addAnimation(speedometer_animation2)

        pa_group = QParallelAnimationGroup(self)
        pa_group.addAnimation(check_all_state_animation)
        pa_group.addAnimation(sa_speeddial_group)

        sa_group = QSequentialAnimationGroup(self)
        sa_group.addAnimation(indicator_animation)
        sa_group.addAnimation(header_animation)
        sa_group.addAnimation(speedometer_popup_animation)
        sa_group.addAnimation(pa_group)
        sa_group.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    def indicator_animation(self, pos):
        self.scaled_header_border.translate(0, -self.scaled_header_border.boundingRect().y()-self.scaled_header_border.boundingRect().height())
        self.scaled_header_inner.translate(0, -self.scaled_header_inner.boundingRect().y()-self.scaled_header_border.boundingRect().height())
        # left indicator
        self.scaled_left_idicator.translate(-self.scaled_left_idicator.boundingRect().x(), -self.scaled_left_idicator.boundingRect().y())
        self.scaled_left_idicator.translate(pos, self.height()*0.06)
        # right indicator
        self.scaled_right_idicator.translate(-self.scaled_right_idicator.boundingRect().x(), -self.scaled_right_idicator.boundingRect().y())
        self.scaled_right_idicator.translate(self.width()-self.scaled_right_idicator.boundingRect().width()-self.scaled_left_idicator.boundingRect().x(), self.height()*0.06)
        self.repaint()

    def header_animation(self, pos):
        self.scaled_header_border.translate(0, -self.scaled_header_border.boundingRect().y()-self.scaled_header_border.boundingRect().height())
        self.scaled_header_inner.translate(0, -self.scaled_header_inner.boundingRect().y()-self.scaled_header_border.boundingRect().height())
        self.scaled_header_border.translate(0, pos)
        self.scaled_header_inner.translate(0, pos)
        self.repaint()

    def speedometer_popup_animation(self, pos):
        self.speedometer_bounding_rect.moveTop(pos)
        self.repaint()

    def other_popup_animation(self):
        self.other_visible = True
        self.repaint()

    def speedometer_animation(self, val):
        self.speed = val
        self.repaint()

    def check_all_state_animation(self, loop_count):
        if loop_count == 1:
            self.show_time = 1
        elif loop_count == 2:
            self.left_indicator_color = self.indicator_color_list[1]
        elif loop_count == 3:
            self.left_indicator_color = self.indicator_color_list[0]
            self.header_border_color = 1
        elif loop_count == 4:
            self.header_border_color = 0
            self.right_indicator_color = self.indicator_color_list[1]
        elif loop_count == 5:
            self.right_indicator_color = self.indicator_color_list[0]
            self.set_horn_state(1)
        elif loop_count == 6:
            self.set_horn_state(0)
            self.charge_state = 1
        elif loop_count == 7:
            if not self.charge_default_state:
                self.charge_state = 0
            self.break_state = 1
        elif loop_count == 8:
            self.break_state = 0
            self.accelerator_state = 1
        elif loop_count == 9:
            self.accelerator_state = 0
        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(_RENDER_HINTS, True)

        linearGradient = QLinearGradient(self.rect().topLeft(), self.rect().bottomRight())
        linearGradient.setColorAt(0.2, QColor(0, 0, 0))
        linearGradient.setColorAt(0.7, QColor(16,0,0))
        linearGradient.setColorAt(0.5, QColor(56,0,0))

        painter.setBrush(linearGradient)
        painter.drawRect(self.rect())

        self.header_painting(painter)
        self.indicators_painting(painter)
        if self.other_visible:
            self.horn_painting(painter)
            self.charge_painting(painter)
            self.break_painting(painter)
            self.accelerator_painting(painter)
        self.speedometer_painting(painter)
        self.battery_indicator_painting(painter)


class _DashBoardControls(QObject):
    """WARNING: This is a private class. do not import this."""
    set_speedometer_range_sig = pyqtSignal(int)
    accelerator_sig = pyqtSignal(int)
    set_current_speed_signal = pyqtSignal(int)
    set_speedometer_resetter_sig = pyqtSignal(int)
    break_sig = pyqtSignal(int)
    horn_sig = pyqtSignal(int)
    indicator_sig = pyqtSignal(int)
    set_battery_remaining_power_sig = pyqtSignal(int)
    charging_sig = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        global _dash_board
        
        self.required_values()

        if _dash_board is not None:
            self.dash_board = _dash_board
            self.startup_values_setter()
            if __name__ == "__main__":  # for install default key event if dashboard called in main thread
                self.dash_board.installEventFilter(self.dash_board) 
            self.all_connector()

    def required_values(self):
        # default keys to prevent error
        self.keys_ = {Qt.Key.Key_W: False, Qt.Key.Key_H: False, Qt.Key.Key_Left: False, 
                        Qt.Key.Key_Right: False, Qt.Key.Key_Space: False, Qt.Key.Key_Escape: False}
        self.dashboard_height = 720
        self.dashboard_width = 1280
        self.creator_btn_hide = False
        self.start_skip = False
        self.loading_skip = False
        self.speedometer_topspeed = 200
        self.battery_level = 100
        self.charging_state = 0 # off

    def startup_values_setter(self):
        self.keys_ = self.dash_board.keys_  # orginal keys
        self.dash_board.dash_board_design_widget.set_speedometer_range(self.speedometer_topspeed)
        self.dash_board.dash_board_design_widget.set_battery(self.battery_level)
        self.dash_board.dash_board_design_widget.set_charge_state(self.charging_state)

    def launch_dashboard(self):
        app = QApplication(sys.argv)
        self.dash_board = _DashBoardMain(None, (self.dashboard_width, self.dashboard_height), \
                                            self.creator_btn_hide, self.start_skip, self.loading_skip)
        self.startup_values_setter()
        if __name__ == "__main__":  # for install default key event if dashboard called in main thread
            self.dash_board.installEventFilter(self.dash_board) 
        self.all_connector()
        self.dash_board.show()
        app.exec()

    def all_connector(self):
        self.set_speedometer_range_sig.connect(self.dash_board.dash_board_design_widget.set_speedometer_range)
        self.accelerator_sig.connect(self.dash_board.dash_board_design_widget.set_accelerator_state)
        self.set_current_speed_signal.connect(self.dash_board.dash_board_design_widget.set_speed)
        self.set_speedometer_resetter_sig.connect(self.dash_board.dash_board_design_widget.set_speedometer_resetter_state)
        self.break_sig.connect(self.dash_board.dash_board_design_widget.set_break_state)
        self.horn_sig.connect(self.dash_board.dash_board_design_widget.set_horn_state)
        self.indicator_sig.connect(self.dash_board.dash_board_design_widget.indicator_triger)
        self.set_battery_remaining_power_sig.connect(self.dash_board.dash_board_design_widget.set_battery)
        self.charging_sig.connect(self.dash_board.dash_board_design_widget.set_charge_state)

    def set_dashboard_size(self, width, height):
        self.dashboard_height = height
        self.dashboard_width = width

    def hide_creator_button(self, hide):
        self.creator_btn_hide = hide

    def skip_start_screen(self, skip):
        self.start_skip = skip

    def skip_loading_screen(self, skip):
        self.loading_skip = skip

    def set_speedometer_range(self, top_speed):
        self.speedometer_topspeed = top_speed
        self.set_speedometer_range_sig.emit(top_speed)

    def apply_accelerator(self):
        self.keys_[Qt.Key.Key_W] = True
        self.accelerator_sig.emit(1)

    def release_accelerator(self):
        self.keys_[Qt.Key.Key_W] = False
        self.accelerator_sig.emit(0)

    def set_speed(self, current_speed):
        self.set_current_speed_signal.emit(current_speed)

    def set_speedometer_resetter_state(self, state):
        self.set_speedometer_resetter_sig.emit(state)

    def apply_break(self):
        self.keys_[Qt.Key.Key_Space] = True
        self.break_sig.emit(1)

    def release_break(self):
        self.keys_[Qt.Key.Key_Space] = False
        self.break_sig.emit(0)

    def sound_horn(self):
        self.keys_[Qt.Key.Key_H] = True
        self.horn_sig.emit(1)

    def off_horn(self):
        self.keys_[Qt.Key.Key_H] = False
        self.horn_sig.emit(0)

    def left_indicator_on_or_off(self):
        self.keys_[Qt.Key.Key_Left] = True
        self.indicator_sig.emit(0)

    def right_indicator_on_or_off(self):
        self.keys_[Qt.Key.Key_Right] = True
        self.indicator_sig.emit(1)

    def update_battery_power(self, current_battery_power):
        self.battery_level = current_battery_power
        self.set_battery_remaining_power_sig.emit(current_battery_power)

    def charging_on(self):
        self.charging_state = 1
        self.charging_sig.emit(1)

    def charging_off(self):
        self.charging_state = 0
        self.charging_sig.emit(0)


class DashBoard(QWidget):
    """This is a pyqt widget class to embed this dashboard to other pyqt widgets"""
    def __init__(self, parent=None):
        super(DashBoard, self).__init__(parent)
        
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

    def show_dashboard(self, hide_creator_button: bool = False, skip_start_screen: bool = False, 
                        skip_loading_screen: bool = False):
        """This method is to show the dashboard in your window"""
        global _dash_board
        
        self.dash_board_widget = _DashBoardMain(self, (self.width(), self.height()), hide_creator_button, skip_start_screen, skip_loading_screen, True)
        self.dash_board_widget.move(0, 0)
        self.vlayout.addWidget(self.dash_board_widget)
        
        _dash_board = self.dash_board_widget


class TriggerAction():
    """This class contain all functionality settings of dashboard \
        including lunch_dashboard() method to show dashboard as seperate window"""
    def __init__(self):
        self.__dbc = _DashBoardControls()

    def launch_dashboard(self):
        """Open dashboard window"""
        self.__dbc.launch_dashboard()

    def set_dashboard_size(self, width: int, height: int):
        """Size should be aspect ratio of width:height = 16:9 \n note: this method should \
            be called before you call launch_dashboard() method to take effect"""
        if height is not None and width is not None:
            self.__dbc.set_dashboard_size(width, height)

    def hide_creator_button(self, hide: bool):
        """To hide creator button on start screen \n note: this method should \
            be called before you call launch_dashboard() method to take effect"""
        self.__dbc.hide_creator_button(hide)

    def skip_start_screen(self, skip: bool):
        """Skip start screen and directly go to loding screen \n note: this method should \
            be called before you call launch_dashboard() method to take effect"""
        self.__dbc.skip_start_screen(skip)

    def skip_loading_screen(self, skip: bool):
        """Skip loading screen and directly go to dashboard screen \n note: this method should \
            be called before you call launch_dashboard() method to take effect"""
        self.__dbc.skip_loading_screen(skip)

    def set_speedometer_range(self, top_speed: int):
        """Set speedometer range (i.e.) 0 to top speed \n
        Note: given value should be between 40 to 400 and the given value \
        will internally converted to nearest multiple of 20"""
        self.__dbc.set_speedometer_range(top_speed)

    def apply_accelerator(self):
        """To activate accelerator"""
        self.__dbc.apply_accelerator()

    def release_accelerator(self):
        """To deactivate accelerator"""
        self.__dbc.release_accelerator()

    def set_speed(self, current_speed: int):
        """The speed should be between 0 to top speed available in speedometer. To \
        set speedometer range use set_speedometer_range() method \n note: if you have \
        speedometer, then call set_speedometer_resetter_state() method and pass 'True' \
        after call this set_speed() method and pass current speed value each time when \
        speedometer update"""
        self.__dbc.set_speed(current_speed)

    def set_speedometer_resetter_state(self, state: bool):
        """To turn on or off speedometer reset internal function to 0 kmph after accelerator release \n note: set state True when \
        you did not have speedometer to update the current speed else set state False when you have speedometer to update current speed"""
        self.__dbc.set_speedometer_resetter_state(state)

    def apply_break(self):
        """To activate break"""
        self.__dbc.apply_break()

    def release_break(self):
        """To deactivate break"""
        self.__dbc.release_break()

    def sound_horn(self):
        """To activate horn"""
        self.__dbc.sound_horn()

    def off_horn(self):
        """To deactivate horn"""
        self.__dbc.off_horn()

    def left_indicator_on_or_off(self):
        """Blink left indicator \n note: call this function \
            again to invert current state of left indicator"""
        self.__dbc.left_indicator_on_or_off()

    def right_indicator_on_or_off(self):
        """Blink right indicator \n note: call this function \
            again to invert current state of right indicator"""
        self.__dbc.right_indicator_on_or_off()

    def update_battery_power(self, current_battery_power: int):
        """To set current battery power \n note: Value should be between 0 to 100"""
        self.__dbc.update_battery_power(current_battery_power)

    def charging_on(self):
        """To indicate charging is on"""
        self.__dbc.charging_on()

    def charging_off(self):
        """To indicate charging is off"""
        self.__dbc.charging_off()


# main
if __name__ == "__main__":
    ta = TriggerAction()
    ta.launch_dashboard()