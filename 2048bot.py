import random
import copy
import math
import dico
import traceback
import sys
from dico_interaction import InteractionClient, InteractionContext


class UndefinedDirectionError(Exception):
    def __init__(self):
        super().__init__('UndefinedDirectionError')


class FinishedGameError(Exception):
    def __init__(self):
        super().__init__('The game has already over.')


class Class2048:
    def __init__(self, msg_id, author_id):
        self.sq = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.score = 0
        self.over = False
        self.__randomSpawn()
        self.__randomSpawn()

        self.bot_msg_id = msg_id
        self.author_id = author_id

    def __isGameOver(self):
        cnt = 0
        sw = [0, 1, -1]
        ne = [0, 1, -1]

        for i in range(0, 4):
            for j in range(0, 4):
                tmp_cnt, tmp_chk = 0, 0
                for x in range(0, 3):
                    for y in range(0, 3):
                        if (sw[x] + i > -1 and sw[x] + i < 4 and ne[y] + j > -1 and ne[y] + j < 4 and (
                                abs(sw[x]) + abs(ne[y]) == 1)):
                            tmp_cnt += 1
                            if (self.sq[sw[x] + i][ne[y] + j] != self.sq[i][j] and self.sq[sw[x] + i][ne[y] + j] != 0):
                                tmp_chk += 1
                if (tmp_chk == tmp_cnt):
                    cnt += 1
        if (cnt == 16):
            return True
        return False

    def __randomSpawn(self):
        while True:
            a, b = random.randrange(0, 4), random.randrange(0, 4)
            spawn = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
            if (self.sq[a][b] == 0):
                self.sq[a][b] = random.choice(spawn)
                break

    def __subMergeUp(self):
        for i in range(0, 4):
            line = []
            for j in range(0, 4): line.append(self.sq[j][i])
            cnt = 0
            for x in range(0, 4):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt += 1
            for x in range(0, 3):
                if (line[x] == line[x + 1]):
                    line[x], line[x + 1] = line[x] + line[x + 1], 0
                    self.score += line[x]
            cnt = 0
            for x in range(0, 4):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt += 1
            for j in range(0, 4): self.sq[j][i] = line[j]

    def __subMergeDown(self):
        for i in range(0, 4):
            line = []
            for j in range(0, 4): line.append(self.sq[j][i])
            cnt = 3
            for x in range(3, -1, -1):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt -= 1
            for x in range(3, 0, -1):
                if (line[x] == line[x - 1]):
                    line[x], line[x - 1] = line[x] + line[x - 1], 0
                    self.score += line[x]
            cnt = 3
            for x in range(3, -1, -1):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt -= 1
            for j in range(0, 4): self.sq[j][i] = line[j]

    def __subMergeLeft(self):
        for i in range(0, 4):
            line = self.sq[i]
            cnt = 0
            for x in range(0, 4):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt += 1
            for x in range(0, 3):
                if (line[x] == line[x + 1]):
                    line[x], line[x + 1] = line[x] + line[x + 1], 0
                    self.score += line[x]
            cnt = 0
            for x in range(0, 4):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt += 1
            self.sq[i] = line

    def __subMergeRight(self):
        for i in range(0, 4):
            line = self.sq[i]
            cnt = 3
            for x in range(3, -1, -1):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt -= 1
            for x in range(3, 0, -1):
                if (line[x] == line[x - 1]):
                    line[x], line[x - 1] = line[x] + line[x - 1], 0
                    self.score += line[x]
            cnt = 3
            for x in range(3, -1, -1):
                if (line[x] != 0):
                    line[cnt] = line[x]
                    if (cnt != x):
                        line[x] = 0
                    cnt -= 1
            self.sq[i] = line

    def merge(self, direction):
        if (self.over):
            raise FinishedGameError
        if (direction == 'up'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeUp()
            if (not prv == self.sq):
                self.__randomSpawn()
        elif (direction == 'down'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeDown()
            if (not prv == self.sq):
                self.__randomSpawn()
        elif (direction == 'left'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeLeft()
            if (not prv == self.sq):
                self.__randomSpawn()
        elif (direction == 'right'):
            prv = copy.deepcopy(self.sq)
            self.__subMergeRight()
            if (not prv == self.sq):
                self.__randomSpawn()
        else:
            raise UndefinedDirectionError

        if (self.__isGameOver()):
            over = True
            return -1

        return 0


# Bot Area

with open('token.txt', 'r') as f:
    token = f.read()

client = dico.Client(token)
interaction = InteractionClient(client=client, auto_register_commands=True, guild_id_lock=670522521682182155)


def create_msg(m):
    buffer = ""
    emojis = ['',
              '<:2:904349077746118706>',
              '<:4:904349077750292520>',
              '<:8:904349078345895946>',
              '<:16:904349077737734144>',
              '<:32:904349077674786816>',
              '<:64:904349077716738068>',
              '<:128:904349077960028191>',
              '<:256:904349077813219328>',
              '<:512:904349078421377044>',
              '<:1024:904349077788049428>',
              '<:2048:904349077062447114>']
    for i in range(0, 4):
        for j in range(0, 4):
            if m[i][j] == 0:
                buffer += '⬛'
            else:
                buffer += emojis[int(math.log2(m[i][j]))]
        buffer += '\n'
    return buffer


emoji_left = "<left:909659546081959956>"
emoji_up = "<up:909659546304249867>"
emoji_down = "<down:909659546182631476>"
emoji_right = "<right:909659546295869450>"
emoji_cancel = "✖"


def create_buttons(message_id, disabled=False):
    left_button = dico.Button(style=dico.ButtonStyles.PRIMARY, emoji=emoji_left, custom_id=f"left{message_id}", disabled=disabled)
    up_button = dico.Button(style=dico.ButtonStyles.PRIMARY, emoji=emoji_up, custom_id=f"up{message_id}", disabled=disabled)
    down_button = dico.Button(style=dico.ButtonStyles.PRIMARY, emoji=emoji_down, custom_id=f"down{message_id}", disabled=disabled)
    right_button = dico.Button(style=dico.ButtonStyles.PRIMARY, emoji=emoji_right, custom_id=f"right{message_id}", disabled=disabled)
    cancel_button = dico.Button(style=dico.ButtonStyles.DANGER, emoji=emoji_cancel, custom_id=f"cancel{message_id}", disabled=disabled)
    row = dico.ActionRow(left_button, up_button, down_button, right_button, cancel_button)
    return row


games = {}


async def game_over(inter, game):
    await inter.send(create_msg(game.sq) + '\nGame Over! Your final score is: ' + str(game.score),
                     components=[create_buttons(inter.message.id, disabled=True)])
    del games[int(inter.message.id)]


@client.on()
async def on_interaction_error(inter: InteractionContext, ex: Exception):
    if isinstance(ex, KeyError):
        await inter.send("Invalid game session. Start new game.")
    else:
        tb = ''.join(traceback.format_exception(type(ex), ex, ex.__traceback__))
        title = f"Exception while executing command {inter.data.name}" if inter.type.application_command else \
            f"Exception while executing callback of {inter.data.custom_id}"
        print(f"{title}:\n{tb}", file=sys.stderr)


@interaction.component_callback("cancel")
async def cancel_button(ctx: InteractionContext):
    game = games.pop(int(ctx.message.id))
    if ctx.author.id != game.author_id:
        return await ctx.send("This is not your session!", ephemeral=True)
    await ctx.send(create_msg(game.sq) + '\nThis game is cancelled. Score: ' + str(game.score),
                   update_message=True, components=[create_buttons(ctx.message.id, disabled=True)])


@interaction.component_callback("left")
async def left_button(ctx: InteractionContext):
    if not ctx.data.component_type.button:
        return
    game = games[int(ctx.message.id)]
    if ctx.author.id != game.author_id:
        return await ctx.send("This is not your session!", ephemeral=True)
    res = game.merge('left')
    if res == -1:
        await game_over(ctx, game)
    else:
        await ctx.send(create_msg(game.sq), update_message=True)


@interaction.component_callback("up")
async def up_button(ctx: InteractionContext):
    if not ctx.data.component_type.button:
        return
    game = games[int(ctx.message.id)]
    if ctx.author.id != game.author_id:
        return await ctx.send("This is not your session!", ephemeral=True)
    res = game.merge('up')
    if res == -1:
        await game_over(ctx, game)
    else:
        await ctx.send(create_msg(game.sq), update_message=True)


@interaction.component_callback("down")
async def down_button(ctx: InteractionContext):
    if not ctx.data.component_type.button:
        return
    game = games[int(ctx.message.id)]
    if ctx.author.id != game.author_id:
        return await ctx.send("This is not your session!", ephemeral=True)
    res = game.merge('down')
    if res == -1:
        await game_over(ctx, game)
    else:
        await ctx.send(create_msg(game.sq), update_message=True)


@interaction.component_callback("right")
async def right_button(ctx: InteractionContext):
    if not ctx.data.component_type.button:
        return
    game = games[int(ctx.message.id)]
    if ctx.author.id != game.author_id:
        return await ctx.send("This is not your session!", ephemeral=True)
    res = game.merge('right')
    if res == -1:
        await game_over(ctx, game)
    else:
        await ctx.send(create_msg(game.sq), update_message=True)


@interaction.slash(name="start", description="Starts a new game.")
async def start(ctx: InteractionContext):
    await ctx.defer()
    msg = await ctx.request_original_response()
    games[int(msg)] = Class2048(int(msg), int(ctx.author))
    await ctx.send(create_msg(games[int(msg)].sq))
    await ctx.edit_original_response(content=create_msg(games[int(msg)].sq), components=[create_buttons(int(msg))])


client.run()

'''
<:2:904349077746118706>
<:4:904349077750292520>
<:8:904349078345895946>
<:16:904349077737734144>
<:32:904349077674786816>
<:64:904349077716738068>
<:128:904349077960028191>
<:256:904349077813219328>
<:512:904349078421377044>
<:1024:904349077788049428>
<:2048:904349077062447114>
⬛
'''

'''
타임아웃 부분 수정하기
대충 여러 게임 돌려도 안 겹치게 만들기
'''
