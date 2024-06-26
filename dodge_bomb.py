import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1200, 800
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
def game_over(screen:pg.Surface):
    """
    こうかとんに爆弾が着弾した際に，
    画面をブラックアウトし，
    泣いているこうかとん画像と
    「Game Over」の文字列を
    5秒間表示させる関数を実装する！
    """
    blackout = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(blackout, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    blackout.set_alpha(128)
    screen.blit(blackout, [0, 0])
    pg.display.update()
    
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rect = txt.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(txt, txt_rect)
    pg.display.update()

    kt_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    kt_rct = kt_img.get_rect()
    kt_rct.center = (900, 400)
    screen.blit(kt_img, kt_rct)
    pg.display.update()

    kt_rct.center = (400, 400)
    screen.blit(kt_img, kt_rct)
    pg.display.update()
    time.sleep(5)


os.chdir(os.path.dirname(os.path.abspath(__file__)))#現在の作業ディレクトリを、現在のスクリプトファイルが存在するディレクトリに変更するためのもの

def check_bound(obj_rct:pg.Rect):
    """
    こうかとんRect：または：爆弾Rectの画面内外用の関数
    引数：こうかとんRect：または：爆弾Rect
    戻り値：横方向判定結果：縦方向判定結果 (True/画面内, False/画面外)   
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey(0)
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct): #こうかとんと爆弾がぶつかったら
            print("Game Over")
            game_over(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
