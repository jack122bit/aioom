import pygame
import numpy as np
import random
import math
import time
import sys

# --- Constants ---
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 30

# --- Map Tile Types ---
T_EMPTY = 0
T_BRICK = 1
T_STONE = 2
T_WOOD = 3
T_METAL = 4
T_EXIT = 9 # Special tile for level exit

# --- Level Data Structure ---
LEVELS = [
    # Level 0
    {
        "map": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 2, 0, 3, 0, 4, 4, 0, 2, 0, 3, 3, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 3, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 3, 0, 0, 1, 0, 1, 0, 4, 4, 4, 4, 9, 0, 1], # Exit Tile (9)
            [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 2, 0, 4, 4, 4, 4, 0, 2, 2, 0, 2, 2, 0, 1],
            [1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
            [1, 0, 2, 2, 2, 2, 0, 2, 2, 2, 2, 0, 3, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
        "player_start": (3.5, 3.5),
        "player_angle": math.pi / 4,
        "sprites": [
            (5.5, 5.5, 10, 1.0, False, 40), (7.5, 2.5, 10, 1.0, False, 40),
            (10.5, 10.5, 11, 0.5, True, 1), (2.5, 8.5, 12, 1.2, False, 80),
        ],
        "music": "level1_music"
    },
    # Level 1 (Will not be reached)
    {
        "map": [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 3, 3, 3, 0, 0, 0, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 3, 9, 3, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 0, 0, 3, 3, 3, 0, 0, 0, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        ],
        "player_start": (1.5, 1.5),
        "player_angle": 0,
        "sprites": [
            (4.5, 4.5, 10, 1.0, False, 40), (6.5, 1.5, 10, 1.0, False, 40),
            (8.5, 8.5, 12, 1.2, False, 80), (1.5, 8.5, 11, 0.5, True, 1),
        ],
         "music": "level2_music"
    },
]
MAX_LEVELS = len(LEVELS)

# --- Global Game State ---
current_level_index = 0
MAP_GRID = []
MAP_WIDTH = 0
MAP_HEIGHT = 0
TILE_SIZE = 64

# --- Player ---
player_x = 3.5
player_y = 3.5
player_angle = math.pi / 4
player_speed = 0.1
player_rot_speed = 0.05
player_health = 100
player_max_health = 100
player_ammo = 50
player_clip_ammo = 10
player_clip_size = 10
player_is_reloading = False
player_reload_start_time = 0
player_reload_time = 1.5
FOV = math.pi / 3

# --- Graphics ---
TEX_WIDTH = 64
TEX_HEIGHT = 64
textures = {}

# --- Sprites ---
sprites = []
sprite_textures = {}

# --- Sound ---
SAMPLE_RATE = 44100
AUDIO_FORMAT = -16
AUDIO_CHANNELS = 2 # Ensure Stereo
AUDIO_BUFFER = 512
music_channel = None

# --- Colors ---
COLOR_FLOOR = (50, 50, 50)
COLOR_CEILING = (70, 70, 120)
COLOR_RED = (200, 0, 0)
COLOR_GREEN = (0, 150, 0)
COLOR_BLUE = (0, 0, 200)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_BROWN = (139, 69, 19)
COLOR_DARK_RED = (100, 0, 0)
COLOR_PINK = (255, 105, 180)
COLOR_DARK_BROWN = (80, 40, 10)
COLOR_DARK_GREY = (40, 40, 40)
COLOR_BRIGHT_RED = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_TRANSPARENT = (255, 0, 255)
COLOR_BLACK = (0, 0, 0)

# --- Win Screen ---
credits_text = [
    "YOU ARE VICTORIOUS!", "", "A Procedural Raycaster Demo", "Inspired by DOOM", "",
    "Created with Python & Pygame", "", "Featuring:", "  Procedural Textures",
    "  Procedural Sprites", "  Procedural Sounds", "", "Thanks for playing!", "", "",
    "Press ESC to Exit"
]
credits_scroll_y = SCREEN_HEIGHT
credits_scroll_speed = 30
generator_textures = []
generator_grid_size = 8
generator_tex_size = SCREEN_WIDTH // generator_grid_size
last_generator_update = 0
generator_update_interval = 0.1

# --- Dummy Sound Class ---
class DummySound:
    def play(self, *args, **kwargs): pass
    def stop(self, *args, **kwargs): pass
    def get_num_channels(self): return 0

# --- Asset Generation ---
def generate_texture(size, base_color, detail_color, pattern='brick'):
    tex = pygame.Surface(size).convert()
    tex.fill(base_color)
    w, h = size
    if pattern == 'brick':
        brick_h = h // 4
        mortar = max(1, h // 32)
        for row in range(4):
            y = row * brick_h
            pygame.draw.rect(tex, detail_color, (0, y, w, mortar))
            offset = w // 2 if row % 2 == 1 else 0
            for col in range(2):
                 x = offset + col * w // 2
                 pygame.draw.rect(tex, detail_color, (x, y, mortar, brick_h))
    elif pattern == 'stone':
        for _ in range(int(w * h * 0.05)):
             spot_size=random.randint(w//16, w//8)
             sx=random.randint(0,w-spot_size)
             sy=random.randint(0,h-spot_size)
             pygame.draw.rect(tex, detail_color, (sx, sy, spot_size, spot_size), border_radius=2)
    elif pattern == 'wood':
        for i in range(w // 4):
            x = i * 4 + random.randint(-5, 5)
            pygame.draw.line(tex, detail_color, (x, 0), (x+random.randint(-2,2), h), 1)
    elif pattern == 'metal':
        panel_w = w // 4
        rivet_size = max(1, w // 32)
        for col in range(4):
            x = col * panel_w
            pygame.draw.rect(tex, detail_color, (x, 0, max(1, w//64), h))
            for row in range(h // panel_w):
                y = row * panel_w + panel_w // 2
                pygame.draw.circle(tex, detail_color, (x + panel_w // 2, y), rivet_size)
    elif pattern == 'exit':
        tex.fill((0,0,0))
        pygame.draw.rect(tex, detail_color, (w*0.2, h*0.1, w*0.6, h*0.8))
        pygame.draw.polygon(tex, base_color, [(w*0.3, h*0.5), (w*0.7, h*0.2), (w*0.7, h*0.8)])
    elif pattern == 'imp':
        tex.fill(COLOR_DARK_BROWN)
        # Use detail_color passed to the function if available, else default
        imp_detail = detail_color if detail_color else (100, 60, 20) # Slightly lighter brown
        pygame.draw.circle(tex, imp_detail, (w//2, h//4), w//6)
        pygame.draw.rect(tex, imp_detail, (w*0.3, h*0.4, w*0.4, h*0.5), border_radius=w//10)
        pygame.draw.circle(tex, COLOR_RED, (w//2-w//12, h//4), w//24)
        pygame.draw.circle(tex, COLOR_RED, (w//2+w//12, h//4), w//24)
    elif pattern == 'demon':
        tex.fill(COLOR_PINK)
        demon_detail = detail_color if detail_color else (200, 80, 150) # Slightly darker pink
        pygame.draw.rect(tex, demon_detail, (w*0.1, h*0.2, w*0.8, h*0.7), border_radius=w//5)
        pygame.draw.rect(tex, COLOR_DARK_RED, (w*0.3, h*0.7, w*0.4, h*0.1))
    elif pattern == 'pickup_health':
        tex.fill(base_color)
        pygame.draw.rect(tex, detail_color, (w*0.3, h*0.1, w*0.4, h*0.8)) # Use detail_color for the '+'
        pygame.draw.rect(tex, detail_color, (w*0.1, h*0.3, w*0.8, h*0.4))
    elif pattern == 'dead_body':
        tex.fill(COLOR_DARK_GREY)
        splatter_color = detail_color if detail_color else COLOR_DARK_RED # Use detail_color for splatter
        for _ in range(5):
            cx, cy = random.randint(w//4, 3*w//4), random.randint(h//4, 3*h//4)
            r = random.randint(w//10, w//5)
            pygame.draw.circle(tex, splatter_color, (cx,cy), r)
    return tex

def generate_alpha_texture(size, base_color, detail_color, pattern='imp'):
    tex = pygame.Surface(size, pygame.SRCALPHA).convert_alpha(); tex.fill((0,0,0,0)); w,h=size
    if pattern == 'imp':
        body,eye=COLOR_DARK_BROWN,COLOR_BRIGHT_RED
        pygame.draw.rect(tex, body, (w*0.3,h*0.4,w*0.4,h*0.5), border_radius=w//10)
        pygame.draw.circle(tex, body, (w//2,h//4), w//5)
        pygame.draw.circle(tex, eye, (w//2-w//12,h//4), w//24)
        pygame.draw.circle(tex, eye, (w//2+w//12,h//4), w//24)
    elif pattern == 'demon':
        body,mouth=COLOR_PINK,COLOR_DARK_RED
        pygame.draw.rect(tex, body, (w*0.1,h*0.2,w*0.8,h*0.7), border_radius=w//5)
        pygame.draw.rect(tex, mouth, (w*0.3,h*0.7,w*0.4,h*0.1))
    elif pattern == 'pickup_health':
        base = base_color if base_color else COLOR_WHITE # Use provided base or default
        plus = detail_color if detail_color else COLOR_RED   # Use provided detail or default
        pygame.draw.rect(tex, base, (w*0.1,h*0.1,w*0.8,h*0.8), border_radius=w//10)
        pygame.draw.rect(tex, plus, (w*0.3,h*0.2,w*0.4,h*0.6))
        pygame.draw.rect(tex, plus, (w*0.2,h*0.3,w*0.6,h*0.4))
    elif pattern == 'dead_body':
        body=COLOR_DARK_GREY
        splat=detail_color if detail_color else COLOR_DARK_RED # Use provided detail or default
        pygame.draw.ellipse(tex, body, (w*0.2,h*0.3,w*0.6,h*0.4))
        for _ in range(5):
            cx,cy=random.randint(w//4,3*w//4),random.randint(h//4,3*h//4)
            r=random.randint(w//10,w//5)
            pygame.draw.circle(tex, splat, (cx,cy), r)
    return tex

def generate_sound(frequency=440, duration=0.1, attack=0.01, decay=0.05, sustain_level=0.1, release=0.02,
                   volume=0.1, waveform='sine', noise_factor=0.0, pitch_bend=0.0, fm_freq=0.0, fm_amp=0.0):
    num_samples = int(duration * SAMPLE_RATE);
    if num_samples <= 0: return DummySound()
    t=np.linspace(0,duration,num_samples,endpoint=False); mod=fm_amp*np.sin(fm_freq*2*np.pi*t) if fm_freq>0 else 0
    freq=frequency*(1+pitch_bend*(t/duration))+mod; freq=np.maximum(20,freq); phase=np.cumsum(freq*2*np.pi/SAMPLE_RATE)
    wave=np.sin(phase)
    if waveform=='square': wave=np.sign(np.sin(phase))
    elif waveform=='sawtooth': wave=2*(phase/(2*np.pi)%1)-1
    elif waveform=='triangle': wave=2*np.abs(2*(phase/(2*np.pi)%1)-1)-1
    elif waveform=='noise': wave=np.random.uniform(-1,1,num_samples)
    if noise_factor>0: noise=np.random.uniform(-1,1,num_samples)*noise_factor; wave=np.clip(wave*(1-noise_factor)+noise,-1,1)
    a,d,r=max(1,int(attack*SAMPLE_RATE)),max(1,int(decay*SAMPLE_RATE)),max(1,int(release*SAMPLE_RATE))
    total_len=a+d+r
    if total_len>num_samples and total_len>0: scale=num_samples/total_len; a=max(1,int(a*scale)); d=max(1,int(d*scale)); r=max(1,num_samples-a-d)
    s=max(0,num_samples-a-d-r); env=np.zeros(num_samples); i1=0
    if a>0: env[:a]=np.linspace(0,1,a); i1=a
    i2=i1
    if d>0 and i1<num_samples: env_d=np.linspace(1,sustain_level,d); i2=i1+d; end_d=min(i2,num_samples); len_d=end_d-i1;
    if len_d>0: env[i1:end_d]=env_d[:len_d]
    i3=i2
    if s>0 and i2<num_samples: i3=i2+s; env[i2:min(i3,num_samples)]=sustain_level
    if r>0 and i3<num_samples: sl=env[i3-1] if i3>0 else 0; env_r=np.linspace(sl,0,r); end_r=min(i3+r,num_samples); len_r=end_r-i3;
    if len_r>0: env[i3:end_r]=env_r[:len_r]
    if len(env)!=len(wave): env=np.pad(env,(0,max(0,len(wave)-len(env))),'edge')[:len(wave)]
    wave*=env; wave=np.clip(wave*volume,-1,1); sound_data=(wave*32767).astype(np.int16)
    if AUDIO_CHANNELS==2:
        if sound_data.ndim==1: sound_data=np.column_stack((sound_data,sound_data))
        elif sound_data.shape[1]==1: sound_data=np.column_stack((sound_data[:,0],sound_data[:,0]))
    try: return pygame.sndarray.make_sound(np.ascontiguousarray(sound_data))
    except Exception as e: print(f"Error making sound: {e}"); return DummySound()

# --- Sprite Class ---
class Sprite:
    def __init__(self, x, y, texture_index, scale=1.0, static=True, health=30):
        self.x, self.y=x,y; self.texture_index=texture_index; self.scale=scale; self.static=static
        self.health,self.max_health=health,health; self.alive=True; self.dist_sq=0

    def update(self, player_x, player_y, dt):
        if not self.static and self.alive:
            dx,dy=player_x-self.x,player_y-self.y; dist=math.hypot(dx,dy)
            if 1.5<dist<8.0 and dist>1e-6:
                 speed=0.02*(1+random.uniform(-0.2,0.2))
                 nx,ny=self.x+(dx/dist)*speed,self.y+(dy/dist)*speed; mx,my=int(nx),int(ny)
                 if 0<=mx<MAP_WIDTH and 0<=my<MAP_HEIGHT and MAP_GRID[my][mx]==T_EMPTY: self.x,self.y=nx,ny

    def take_damage(self, amount, sounds_dict):
        if not self.alive: return False
        self.health-=amount
        if self.health<=0: self.alive,self.health=False,0; print("Sprite died!"); sounds_dict.get('enemy_death',DummySound()).play(); return True
        else: sounds_dict.get('enemy_pain',DummySound()).play(); return False

# --- Game Functions ---
def load_level(level_index):
    global MAP_GRID,MAP_WIDTH,MAP_HEIGHT,player_x,player_y,player_angle,sprites
    if 0<=level_index<MAX_LEVELS:
        ld=LEVELS[level_index]; MAP_GRID=[r[:] for r in ld["map"]]; MAP_WIDTH,MAP_HEIGHT=len(MAP_GRID[0]),len(MAP_GRID)
        player_x,player_y=ld["player_start"]; player_angle=ld["player_angle"]
        sprites.clear(); [sprites.append(Sprite(*sd)) for sd in ld["sprites"]]
        print(f"Loaded Level {level_index}"); return True
    else: print(f"Error: Invalid level index {level_index}"); return False

def play_level_music(level_index, sounds_dict):
    global music_channel; print(f"Placeholder: Music '{LEVELS[level_index]['music']}'")
    if music_channel: music_channel.stop()
    # mt=sounds_dict.get(LEVELS[level_index]['music']); if mt: music_channel=pygame.mixer.find_channel(True); if music_channel: music_channel.play(mt, loops=-1)

def render_game_won_screen(screen, dt, font):
    global credits_scroll_y,last_generator_update,generator_textures
    current_time=time.time(); screen.fill(COLOR_BLACK)
    if current_time-last_generator_update > generator_update_interval:
        last_generator_update=current_time;
        r_col1=(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        r_col2=(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        p=random.choice(['brick','stone','wood','metal','imp','demon']); new_tex=generate_texture((generator_tex_size,generator_tex_size),r_col1,r_col2,p)
        generator_textures.append(new_tex);
        if len(generator_textures)>generator_grid_size**2*2: generator_textures.pop(0)
    ti=0
    for y in range(generator_grid_size):
        for x in range(generator_grid_size):
            if ti<len(generator_textures): screen.blit(generator_textures[len(generator_textures)-1-ti],(x*generator_tex_size,y*generator_tex_size))
            ti+=1
    if font:
        lh=font.get_linesize(); cy=int(credits_scroll_y)
        for line in credits_text:
            if line: ts=font.render(line,1,COLOR_WHITE); tr=ts.get_rect(center=(SCREEN_WIDTH//2,cy));
            if tr.bottom>0 and tr.top<SCREEN_HEIGHT: screen.blit(ts,tr)
            cy+=lh
        credits_scroll_y-=credits_scroll_speed*dt; total_h=len(credits_text)*lh
        if credits_scroll_y<-total_h: credits_scroll_y=SCREEN_HEIGHT

# --- Main Game ---
def main():
    global player_x, player_y, player_angle, sprites, current_level_index
    global player_health, player_ammo, player_clip_ammo, player_is_reloading, player_reload_start_time
    global credits_scroll_y, last_generator_update

    pygame.init(); pygame.font.init(); mixer_initialized=False
    try: pygame.mixer.init(SAMPLE_RATE,AUDIO_FORMAT,AUDIO_CHANNELS,AUDIO_BUFFER); pygame.mixer.set_num_channels(16); mixer_initialized=True; print(f"Mixer:{pygame.mixer.get_init()}")
    except pygame.error as e: print(f"Mixer Error:{e}. Sound disabled.")

    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT)); pygame.display.set_caption("Pygame Raycaster")
    clock=pygame.time.Clock(); hud_font=pygame.font.Font(None,30) if pygame.font.get_init() else None
    msg_font=pygame.font.Font(None,40) if pygame.font.get_init() else None; credits_font=pygame.font.Font(None,28) if pygame.font.get_init() else hud_font
    sounds={} # Initialize sounds locally
    game_msg, game_msg_timer = "", 0 # Initialize messages locally

    print("Generating assets..."); textures.clear(); sprite_textures.clear()
    textures[T_BRICK]=generate_texture((TEX_WIDTH,TEX_HEIGHT),(150,50,50),(100,30,30),'brick'); textures[T_STONE]=generate_texture((TEX_WIDTH,TEX_HEIGHT),(100,100,100),(70,70,70),'stone')
    textures[T_WOOD]=generate_texture((TEX_WIDTH,TEX_HEIGHT),(180,120,80),(130,90,50),'wood'); textures[T_METAL]=generate_texture((TEX_WIDTH,TEX_HEIGHT),(80,80,150),(50,50,100),'metal')
    textures[T_EXIT]=generate_texture((TEX_WIDTH,TEX_HEIGHT),(0,0,50),(200,200,255),'exit'); sprite_textures[10]=generate_alpha_texture((TEX_WIDTH,TEX_HEIGHT),None,None,'imp')
    sprite_textures[11]=generate_alpha_texture((TEX_WIDTH,TEX_HEIGHT),None,None,'pickup_health'); sprite_textures[12]=generate_alpha_texture((TEX_WIDTH,TEX_HEIGHT),None,None,'demon')
    sprite_textures[99]=generate_alpha_texture((TEX_WIDTH,TEX_HEIGHT),None,COLOR_DARK_RED,'dead_body')
    if mixer_initialized:
        sounds['shoot']=generate_sound(frequency=150,duration=0.15,volume=0.15,waveform='sawtooth',noise_factor=0.5,attack=0.005,decay=0.1,release=0.04)
        sounds['reload']=generate_sound(frequency=200,duration=0.4,volume=0.2,waveform='noise',noise_factor=0.3,attack=0.05,decay=0.3)
        sounds['no_ammo']=generate_sound(frequency=600,duration=0.08,volume=0.1,waveform='square',attack=0.01,decay=0.06)
        sounds['hit_wall']=generate_sound(frequency=800,duration=0.05,volume=0.1,waveform='noise',noise_factor=0.8,attack=0.002,decay=0.04)
        sounds['enemy_pain']=generate_sound(frequency=450,duration=0.2,volume=0.2,waveform='square',noise_factor=0.3,pitch_bend=-0.2)
        sounds['enemy_death']=generate_sound(frequency=150,duration=0.6,volume=0.25,waveform='noise',fm_freq=30,fm_amp=80,noise_factor=0.6)
        sounds['level_complete']=generate_sound(frequency=440,duration=1.0,volume=0.3,waveform='sine',attack=0.01,decay=0.8,fm_freq=5,fm_amp=20)
        sounds['pickup']=generate_sound(frequency=660,duration=0.2,volume=0.2,waveform='triangle',attack=0.01,decay=0.15)
        sounds['player_pain']=generate_sound(frequency=300,duration=0.3,volume=0.25,waveform='sine',pitch_bend=-0.5,noise_factor=0.1)
    else: sounds={k:DummySound() for k in ['shoot','reload','no_ammo','hit_wall','enemy_pain','enemy_death','level_complete','pickup','player_pain']}
    print("Assets generated.")

    current_level_index=0;
    if not load_level(current_level_index): print("FATAL: No levels."); pygame.quit(); sys.exit()
    # play_level_music(current_level_index, sounds)

    running=True; show_map=False; game_over=False; game_won=False
    lp_pain_t=0; p_pain_cd=0.5; depth_buffer=np.full(SCREEN_WIDTH,float('inf'),dtype=float)
    shoot_cd=0.2; last_shot_t=0; credits_scroll_y=SCREEN_HEIGHT; last_gen_update=0

    while running:
        dt=clock.tick(FPS)/1000.0; dt=min(dt,0.1); current_time=time.time()

        # Events
        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE: running=False
                if not game_won and not game_over:
                    if event.key==pygame.K_m: show_map=not show_map
                    if event.key==pygame.K_r and not player_is_reloading and player_clip_ammo<player_clip_size and player_ammo>0:
                        player_is_reloading=True; player_reload_start_time=current_time; sounds.get('reload',DummySound()).play()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and not player_is_reloading and not game_over and not game_won:
                if player_clip_ammo>0:
                    if current_time-last_shot_t>=shoot_cd:
                        last_shot_t=current_time; player_clip_ammo-=1; sounds.get('shoot',DummySound()).play()
                        dirX_s,dirY_s=math.cos(player_angle),math.sin(player_angle); dist,max_d,step=0.05,20.0,0.05; hit_sp,hit_w=None,False
                        while dist<max_d:
                            cx,cy=player_x+dirX_s*dist,player_y+dirY_s*dist; mx,my=int(cx),int(cy)
                            if not(0<=mx<MAP_WIDTH and 0<=my<MAP_HEIGHT): hit_w=True; break
                            if MAP_GRID[my][mx]>T_EMPTY and MAP_GRID[my][mx]!=T_EXIT: hit_w=True; break
                            hits=[]
                            for i,sp in enumerate(sprites):
                                if sp.alive and not sp.static: d_sq=(cx-sp.x)**2+(cy-sp.y)**2;
                                if d_sq<0.3**2: hits.append((d_sq,i))
                            if hits: hits.sort(); hit_sp=sprites[hits[0][1]]; break
                            dist+=step
                        if hit_sp and hit_sp.take_damage(random.randint(8,15),sounds): hit_sp.texture_index=99; hit_sp.static=True
                else: sounds.get('no_ammo',DummySound()).play();
                if not player_is_reloading and player_ammo>0: player_is_reloading=True; player_reload_start_time=current_time; sounds.get('reload',DummySound()).play()

        # State Updates
        if game_won: render_game_won_screen(screen,dt,credits_font if credits_font else hud_font); pygame.display.flip(); continue
        elif game_over:
             screen.fill(COLOR_BLACK)
             if msg_font:
                 msg=msg_font.render("GAME OVER",1,COLOR_RED); r=msg.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2-40)); screen.blit(msg,r)
                 ex=msg_font.render("Press ESC to Exit",1,COLOR_WHITE); r=ex.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2+40)); screen.blit(ex,r)
             pygame.display.flip(); continue
        else: # Normal Play
            if player_is_reloading and current_time-player_reload_start_time>=player_reload_time:
                needed=player_clip_size-player_clip_ammo; load=min(needed,player_ammo); player_clip_ammo+=load; player_ammo-=load; player_is_reloading=False;

            keys=pygame.key.get_pressed(); cos_a,sin_a=math.cos(player_angle),math.sin(player_angle); move_x,move_y=0,0
            if keys[pygame.K_w] or keys[pygame.K_UP]: move_x+=player_speed*cos_a; move_y+=player_speed*sin_a
            if keys[pygame.K_s] or keys[pygame.K_DOWN]: move_x-=player_speed*cos_a; move_y-=player_speed*sin_a
            if keys[pygame.K_a]: move_x+=player_speed*sin_a; move_y-=player_speed*cos_a
            if keys[pygame.K_d]: move_x-=player_speed*sin_a; move_y+=player_speed*cos_a
            npx,npy=player_x+move_x,player_y+move_y; mtx,mty=int(npx),int(npy); target_tile=T_EMPTY
            if 0<=mtx<MAP_WIDTH and 0<=mty<MAP_HEIGHT: target_tile=MAP_GRID[mty][mtx]
            is_wall=target_tile>T_EMPTY and target_tile!=T_EXIT

            if not is_wall: player_x,player_y=npx,npy
            else: # Wall slide
                check_x_map_x = int(player_x + move_x)
                check_x_map_y = int(player_y)
                if 0 <= check_x_map_x < MAP_WIDTH and 0 <= check_x_map_y < MAP_HEIGHT and MAP_GRID[check_x_map_y][check_x_map_x] <= T_EMPTY:
                    player_x += move_x

                check_y_map_x = int(player_x)
                check_y_map_y = int(player_y + move_y)
                if 0 <= check_y_map_x < MAP_WIDTH and 0 <= check_y_map_y < MAP_HEIGHT and MAP_GRID[check_y_map_y][check_y_map_x] <= T_EMPTY:
                    player_y += move_y

            pr_sq,sr_sq=0.3**2,0.3**2
            for sprite in sprites:
                 if sprite.alive:
                     d_sq=(player_x-sprite.x)**2+(player_y-sprite.y)**2
                     if d_sq<pr_sq+sr_sq:
                          if sprite.static and sprite.texture_index==11 and player_health<player_max_health: player_health=min(player_max_health,player_health+25); sprite.alive=False; sounds.get('pickup',DummySound()).play()
                          elif not sprite.static and current_time-lp_pain_t>p_pain_cd:
                              player_health-=5; lp_pain_t=current_time; sounds.get('player_pain',DummySound()).play()
                              if player_health<=0: game_over=True; print("GAME OVER")
                              dx,dy=player_x-sprite.x,player_y-sprite.y; norm=math.hypot(dx,dy)
                              if norm>1e-6: kb=0.1; kx,ky=player_x+(dx/norm)*kb,player_y+(dy/norm)*kb; kmx,kmy=int(kx),int(ky);
                              if 0<=kmx<MAP_WIDTH and 0<=kmy<MAP_HEIGHT and MAP_GRID[kmy][kmx]==T_EMPTY: player_x,player_y=kx,ky

            mcx,mcy=int(player_x),int(player_y)
            if 0<=mcx<MAP_WIDTH and 0<=mcy<MAP_HEIGHT and MAP_GRID[mcy][mcx]==T_EXIT: sounds.get('level_complete',DummySound()).play(); game_won=True; print("YOU WON!"); game_message="YOU ARE VICTORIOUS!"; game_message_timer=current_time+5.0;
            if music_channel: music_channel.stop()

            if keys[pygame.K_LEFT] or keys[pygame.K_q]: player_angle-=player_rot_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_e]: player_angle+=player_rot_speed
            player_angle%=(2*math.pi)

            for sprite in sprites: sprite.update(player_x,player_y,dt)

            # --- Rendering ---
            screen.fill(COLOR_FLOOR); pygame.draw.rect(screen,COLOR_CEILING,(0,0,SCREEN_WIDTH,SCREEN_HEIGHT//2))
            dirX,dirY=math.cos(player_angle),math.sin(player_angle); planeX,planeY=math.sin(player_angle)*0.66,-math.cos(player_angle)*0.66
            depth_buffer.fill(float('inf'))

            # Walls
            for x in range(SCREEN_WIDTH):
                camX=2*x/SCREEN_WIDTH-1; rdx,rdy=dirX+planeX*camX,dirY+planeY*camX; mx,my=int(player_x),int(player_y)
                ddx=abs(1/rdx) if rdx else float('inf'); ddy=abs(1/rdy) if rdy else float('inf')
                sx,sdx=(-1,(player_x-mx)*ddx) if rdx<0 else (1,(mx+1.0-player_x)*ddx); sy,sdy=(-1,(player_y-my)*ddy) if rdy<0 else (1,(my+1.0-player_y)*ddy)
                hit,side,steps,max_steps=0,0,0,60
                while hit==0 and steps<max_steps:
                    if sdx<sdy: sdx+=ddx; mx+=sx; side=0
                    else: sdy+=ddy; my+=sy; side=1
                    steps+=1;
                    if not(0<=mx<MAP_WIDTH and 0<=my<MAP_HEIGHT): hit=1; break
                    if MAP_GRID[my][mx]>T_EMPTY: hit=1
                pwd=float('inf')
                if hit and steps<max_steps:
                    try:
                        if side == 0: pwd = ((mx - player_x + (1 - sx) / 2) / rdx)
                        else: pwd = ((my - player_y + (1 - sy) / 2) / rdy)
                    except ZeroDivisionError: pass
                if pwd<=1e-4: pwd=float('inf')
                depth_buffer[x]=pwd; lh=int(SCREEN_HEIGHT/pwd) if pwd!=float('inf') else 0; ds,de=max(0,-lh//2+SCREEN_HEIGHT//2),min(SCREEN_HEIGHT,lh//2+SCREEN_HEIGHT//2)
                if lh>0 and ds<de:
                    map_valid=(0<=mx<MAP_WIDTH and 0<=my<MAP_HEIGHT); tex_n=MAP_GRID[my][mx] if map_valid and hit else 1; tex=textures.get(tex_n)
                    if tex:
                         wx=(player_y+pwd*rdy) if side==0 else (player_x+pwd*rdx); wx-=math.floor(wx); tx=int(wx*TEX_WIDTH);
                         if side==0 and rdx>0: tx=TEX_WIDTH-tx-1
                         if side==1 and rdy<0: tx=TEX_WIDTH-tx-1
                         tx=max(0,min(TEX_WIDTH-1,tx)); th=de-ds
                         if th>0:
                             try: sc=tex.subsurface(tx,0,1,TEX_HEIGHT); scol=pygame.transform.scale(sc,(1,th)); sh=max(0.2,min(1.0,1.0/(1+pwd*0.1)))*(0.7 if side==1 else 1.0); shc=(int(sh*255),)*3; shcol=scol.copy(); shcol.fill(shc,special_flags=pygame.BLEND_MULT); screen.blit(shcol,(x,ds))
                             except ValueError: pass

            # Sprites
            for sprite in sprites: sprite.dist_sq=(player_x-sprite.x)**2+(player_y-sprite.y)**2
            sprites.sort(key=lambda s:s.dist_sq,reverse=True)
            for sprite in sprites:
                if not sprite.alive and sprite.texture_index!=99: continue
                tex=sprite_textures.get(sprite.texture_index);
                if not tex: continue
                sxr,syr=sprite.x-player_x,sprite.y-player_y; inv_det_d=(planeX*dirY-dirX*planeY);
                if abs(inv_det_d)<1e-9: continue
                inv_det=1.0/inv_det_d; tx=inv_det*(dirY*sxr-dirX*syr); ty=inv_det*(-planeY*sxr+planeX*syr)
                if ty<=0.1: continue
                ssx=int((SCREEN_WIDTH/2)*(1+tx/ty)); tex_h,tex_w=tex.get_height(),tex.get_width()
                sh_raw=(SCREEN_HEIGHT/ty)*sprite.scale; sh=abs(int(sh_raw)); asp=(tex_w/tex_h) if tex_h>0 else 1; sw=abs(int(sh_raw*asp))
                dsy,dey=SCREEN_HEIGHT//2-sh//2,SCREEN_HEIGHT//2+sh//2; dsx,dex=ssx-sw//2,ssx+sw//2
                dsyc,deyc=max(0,dsy),min(SCREEN_HEIGHT,dey); dsxc,dexc=max(0,dsx),min(SCREEN_WIDTH,dex)
                for stripe in range(dsxc,dexc):
                      if ty<depth_buffer[stripe]:
                           if sw<=0: continue
                           tx_x=int((stripe-dsx)*tex_w/sw); tx_x=max(0,min(tex_w-1,tx_x))
                           th=deyc-dsyc
                           if th>0 and sh>0:
                                try:
                                    sc=tex.subsurface(tx_x,0,1,tex_h); scol=pygame.transform.scale(sc,(1,th)); shd=max(0.3,min(1.0,1.0/(1+ty*0.15)))
                                    shcol=scol.copy(); shc=(int(shd*255),)*3; shcol.fill(shc,special_flags=pygame.BLEND_MULT)
                                    if tex.get_colorkey(): shcol.set_colorkey(tex.get_colorkey())
                                    screen.blit(shcol,(stripe,dsyc))
                                except ValueError: pass

            # HUD
            if hud_font:
                hp_c=COLOR_GREEN if player_health>60 else COLOR_YELLOW if player_health>30 else COLOR_RED; hpt=hud_font.render(f"HP:{player_health}",1,hp_c); screen.blit(hpt,(10,SCREEN_HEIGHT-40))
                am_c=COLOR_YELLOW if player_clip_ammo>0 else COLOR_RED; ams="RELOADING" if player_is_reloading else f"AMMO:{player_clip_ammo}/{player_ammo}";
                if player_is_reloading: am_c=COLOR_BLUE;
                amt=hud_font.render(ams,1,am_c); screen.blit(amt,(SCREEN_WIDTH-amt.get_width()-10,SCREEN_HEIGHT-40))
                lvl_t=hud_font.render(f"Level:{current_level_index+1}/{MAX_LEVELS}",1,COLOR_WHITE); screen.blit(lvl_t,(SCREEN_WIDTH//2-lvl_t.get_width()//2,10))
                fpst=hud_font.render(f"FPS:{clock.get_fps():.1f}",1,COLOR_GREEN); screen.blit(fpst,(10,10))

            # Messages
            if game_msg and msg_font and current_time<game_msg_timer: msgs=msg_font.render(game_msg,1,COLOR_YELLOW); msgr=msgs.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//3)); screen.blit(msgs,msgr)
            elif game_msg and current_time>=game_msg_timer: game_msg="" # Clear message

            # Crosshair
            cs=8; cx,cy=SCREEN_WIDTH//2,SCREEN_HEIGHT//2; pygame.draw.line(screen,COLOR_WHITE,(cx-cs,cy),(cx+cs,cy),1); pygame.draw.line(screen,COLOR_WHITE,(cx,cy-cs),(cx,cy+cs),1)

            # Debug Map
            if show_map:
                ms=8; mox=SCREEN_WIDTH-(MAP_WIDTH*ms)-10; moy=10; mr=pygame.Rect(mox-5,moy-5,MAP_WIDTH*ms+10,MAP_HEIGHT*ms+10)
                msurf=pygame.Surface(mr.size,pygame.SRCALPHA); msurf.fill((20,20,20,180)); screen.blit(msurf,mr.topleft)
                for y,row in enumerate(MAP_GRID):
                    for x,tile in enumerate(row): c=(80,80,80); t=textures.get(tile);
                    if t: c=t.get_at((0,0)) if tile!=T_EXIT else (0,255,255); pygame.draw.rect(screen,c,(mox+x*ms,moy+y*ms,ms-1,ms-1))
                pxm,pym=mox+int(player_x*ms),moy+int(player_y*ms); pygame.draw.circle(screen,COLOR_GREEN,(pxm,pym),ms//2)
                ll=ms; cos_a,sin_a=math.cos(player_angle),math.sin(player_angle); ex,ey=pxm+ll*cos_a,pym+ll*sin_a; pygame.draw.line(screen,COLOR_GREEN,(pxm,pym),(ex,ey),1)
                for s in sprites:
                    if s.alive or s.texture_index==99: sxm,sym=mox+int(s.x*ms),moy+int(s.y*ms); sc=COLOR_DARK_RED if s.alive and not s.static else (80,0,0) if not s.alive else COLOR_BLUE; pygame.draw.circle(screen,sc,(sxm,sym),ms//3)

            pygame.display.flip() # Final flip for the normal game state

    # --- Cleanup ---
    if mixer_initialized: pygame.mixer.quit()
    pygame.font.quit(); pygame.quit(); sys.exit()

if __name__ == '__main__':
    try: main()
    except Exception as e:
        print("\n--- UNHANDLED EXCEPTION ---"); import traceback; traceback.print_exc(); print("---------------------------\n")
        try: pygame.mixer.quit()
        except: pass
        try: pygame.font.quit()
        except: pass
        try: pygame.quit()
        except: pass
        sys.exit(1)