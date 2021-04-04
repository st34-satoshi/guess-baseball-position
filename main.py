from enum import IntEnum, Enum
import itertools


class Position(IntEnum):
    Pitcher = 1
    Catcher = 2
    First = 3
    Second = 4
    Third = 5
    Short = 6
    Left = 7
    Center = 8
    Right = 0  # 9 % 9 = 0


class Members(Enum):
    Fuziyama  = '藤山'
    Suzuki    = '鈴木'
    Sakrai    = '桜井'
    Umeda     = '梅田'
    Kikuchi   = '菊池'
    Kinosita  = '木下'
    Matsumura = '松村'
    Ogawa     = '小川'
    Yamada    = '山田'


def solve():
    answers = []  # list of members
    # check all permutations
    for members in itertools.permutations(list(Members), 9):
        if valid_positions(members):
            answers.append(members)
    print(f'number of answers is {len(answers)}')
    # for ans in answers:
    #     # TODO: print members position
    #     print(ans)


def valid_positions(members):
    # check these (height, married) contradiction at last
    taller_dict = {}  # {member: [taller members]}
    for m in members:
        taller_dict[m.value] = []
    married_members = set()
    unmarried_members = set()

    # 1. 藤山はサードと同じアパートに住んでいる
    if members[Position.Third] == Members.Fuziyama:
        return False
    # 2. センターはライトより高身長.
    taller_dict[members[Position.Right].value].append(members[Position.Center])
    # 3. 鈴木の妹はセカンドと婚約中
    if members[Position.Second] == Members.Suzuki:
        return False
    # 4. pass
    # 5. ショート、サード、桜井はよく競馬に行く
    if members[Position.Third] == Members.Sakrai or members[Position.Short] == Members.Sakrai:
        return False
    # 6. ピッチャーは梅田と菊池に麻雀で勝つ
    if members[Position.Pitcher] in [Members.Umeda, Members.Kikuchi]:
        return False
    # 7. 外野の1人は木下か松村
    if Members.Kinosita not in [members[Position.Left], members[Position.Center], members[Position.Right]] and \
            Members.Matsumura not in [members[Position.Left], members[Position.Center], members[Position.Right]]:
        return False
    # 8. 小川選手は既婚
    married_members.add(Members.Ogawa)
    # 9. 梅田・藤山・桜井はキャッチャーとセカンドにゴルフで勝てない
    if members[Position.Catcher] in [Members.Umeda, Members.Fuziyama, Members.Sakrai] or \
            members[Position.Second] in [Members.Umeda, Members.Fuziyama, Members.Sakrai]:
        return False
    # 10. ピッチャーは既婚
    married_members.add(members[Position.Pitcher])
    # 11.a. 松村はキャッチャーと仲が良い
    if members[Position.Catcher] == Members.Matsumura:
        return False
    # 11.b. 桜井はピッチャーと仲が良い
    if members[Position.Pitcher] == Members.Sakrai:
        return False
    # 12. 独身は鈴木・梅田・山田・センター・ライト
    if members[Position.Center] in [Members.Suzuki, Members.Umeda, Members.Yamada] or \
            members[Position.Right] in [Members.Suzuki, Members.Umeda, Members.Yamada]:
        return False
    for m in [Members.Suzuki, Members.Umeda, Members.Yamada, members[Position.Center], members[Position.Right]]:
        unmarried_members.add(m)
    # 13. 山田>桜井、木下<桜井、山田,桜井,木下<ファースト
    if members[Position.First] in [Members.Sakrai, Members.Kinosita, Members.Yamada]:
        return False
    taller_dict[Members.Sakrai.value].append(Members.Yamada)
    taller_dict[Members.Kinosita.value].append(Members.Sakrai)
    taller_dict[Members.Sakrai.value].append(members[Position.First])
    taller_dict[Members.Yamada.value].append(members[Position.First])
    taller_dict[Members.Kinosita.value].append(members[Position.First])

    # 14,15,16  TODO: These conditions are not public. So I do not public them here.

    # Check height
    for key, mems in taller_dict.items():
        for taller in mems:
            for taller_v in taller_dict[taller.value]:
                if key == taller_v:
                    return False
    # Check married
    for married in married_members:
        if married in unmarried_members:
            return False
    return True


if __name__ == '__main__':
    solve()

