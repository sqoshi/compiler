import numpy as np


def cmd(command, *r):
    brackets = len(r) * '{} '
    return command.upper() + " " + brackets[:-1].format(*r) + '\n'


def arth1(b):
    a = 17822
    c = 55
    d = 2
    j = 1
    b = b + d
    if b > a:
        t = b
        b = a
        a = t
    else:
        if b == a:
            b = b - j
    for i in np.arange(1001)[1:][::-1]:
        t = b // a
        c = c + t
        c = j * c
        b = d + b
        a = d + a
    print(a)
    print(b)
    print(c)
    print(d)
    print(j)
    print(t)


def arth3(b, c):
    j = 1111111 - 1111110
    if b > 50:
        b = b % 50
    t = b + 1000
    t = t - 1
    print(t)
    for i in range(b, t + 1):
        t = i // j
        c = c + t
        t = i % i
        c = c + t
    print(b)
    print(c)
    print(j)
    print(t)


def arthm2():
    a = 1
    i = 1
    while i <= 1000:
        b = 25663607 + 41445257
        a = b + a
        i = i + 1
    print(a)

    i = 1000
    a = 1
    while True:
        b = 25663607 + 41445257
        a = b + a
        i = i - 1
        if i <= 0:
            break
    print(a)

    a = 11
    for ii in range(1234567830, 1234567801 + 1, -1):
        a = a * 1024
    print(a)
    print(i)
    print(1999999999 * 1999999997)


# 67175972865
# 67108864001
# arthm2()


# print(math.factorial(
#    1000) == 402387260077093773543702433923003985719374864210714632543799910429938512398629020592044208486969404800479988610197196058631666872994808558901323829669944590997424504087073759918823627727188732519779505950995276120874975462497043601418278094646496291056393887437886487337119181045825783647849977012476632889835955735432513185323958463075557409114262417474349347553428646576611667797396668820291207379143853719588249808126867838374559731746136085379534524221586593201928090878297308431392844403281231558611036976801357304216168747609675871348312025478589320767169132448426236131412508780208000261683151027341827977704784635868170164365024153691398281264810213092761244896359928705114964975419909342221566832572080821333186116811553615836546984046708975602900950537616475847728421889679646244945160765353408198901385442487984959953319101723355556602139450399736280750137837615307127761926849034352625200015888535147331611702103968175921510907788019393178114194545257223865541461062892187960223838971476088506276862967146674697562911234082439208160153780889893964518263243671616762179168909779911903754031274622289988005195444414282012187361745992642956581746628302955570299024324153181617210465832036786906117260158783520751516284225540265170483304226143974286933061690897968482590125458327168226458066526769958652682272807075781391858178889652208164348344825993266043367660176999612831860788386150279465955131156552036093988180612138558600301435694527224206344631797460594682573103790084024432438465657245014402821885252470935190620929023136493273497565513958720559654228749774011413346962715422845862377387538230483865688976461927383814900140767310446640259899490222221765904339901886018566526485061799702356193897017860040811889729918311021171229845901641921068884387121855646124960798722908519296819372388642614839657382291123125024186649353143970137428531926649875337218940694281434118520158014123344828015051399694290153483077644569099073152433278288269864602789864321139083506217095002597389863554277196742822248757586765752344220207573630569498825087968928162753848863396909959826280956121450994871701244516461260379029309120889086942028510640182154399457156805941872748998094254742173582401063677404595741785160829230135358081840096996372524230560855903700624271243416909004153690105933983835777939410970027753472000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
# print(math.factorial(
#    100) == 93326215443944152681699238856266700490715968264381621468592963895217599993229915608941463976156518286253697920827223758251185210916864000000000000000000000000)


# 22407395739679346948952902572503159771566152330325298756997544942898194297396703768017371136
# 22407395739679346948952902572503159771566152330325298756997544942898194297396703768017371136

def loop(a=3):
    """> 30000003
> 3000001"""
    b = 10
    c = 1
    d = c * 134217727  # [c(1235) = 2 ^ 27 - 1]
    d = d / 134217727  # ; [c(1235) = 1]
    for k in range(999999, -1, -1):
        for i in [1, 2, 3]:
            a = a + b
            c = c + d
    print(a)
    print(c)


# loop()

def tab2():
    """
    > 10
    > 20
    > 30
    > 40
    > 50
    > 111111111
    > 2
    > 4
    > 6
    > 8
    > 10
    > 111111111
    > 100
    > 80
    > 60
    > 40
    > 20
    > 200
    > 160
    > 120
    > 80
    > 40
    > 300
    > 240
    > 180
    > 120
    > 60
    > 400
    > 320
    > 240
    > 160
    > 80
    > 500
    > 400
    > 300
    > 200
    > 100
    """
    ta = [0 for _ in range(5)]
    tb = [0 for _ in range(5)]
    tc = [0 for _ in range(25)]
    n = 25 - 1
    m = 5 - 1
    z = 0
    for i in range(z, m + 1):
        j = i + 1
        ta[i] = 9 * j
        tb[i] = 6 * j
        tb[i] = tb[i] // 3
        ta[i] = j + ta[i]
    for i in range(z, m + 1):
        print(ta[i])
    print(111111111)
    for i in range(z, m + 1):
        print(tb[i])
    print(111111111)
    for i in range(z, m + 1):
        for k in range(m, z - 1, -1):
            for l in range(z, n + 1):
                j = 5 * i
                j = j + 4
                j = j - k
                if j == l:
                    tc[l] = ta[i] * tb[k]

    for i in range(z, n + 1):
        print(tc[i])


##########################gebala @##############################

def tab5():
    """> 0
        > 24
        > 46
        > 66
        > 84
        > 100
        > 114
        > 126
        > 136
        > 144
        > 150
        > 154
        > 156
        > 156
        > 154
        > 150
        > 144
        > 136
        > 126
        > 114
        > 100
        > 84
        > 66
        > 46
        > 24
        > 0"""
    ta = [0 for _ in range(26)]
    tb = [0 for _ in range(26)]
    tc = [0 for _ in range(26)]
    n = 25
    tc[0] = n
    tc[n] = n - n
    for i in range(tc[0], tc[n] - 1, -1):
        ta[i] = i
        tb[i] = n - i
    for i in range(tc[n], tc[0] + 1):
        tc[i] = ta[i] * tb[i]
    for i in range(0, n + 1):
        print(tc[i])


def sort9():
    """ > 5
    > 2
    > 10
    > 4
    > 20
    > 8
    > 17
    > 16
    > 11
    > 9
    > 22
    > 18
    > 21
    > 13
    > 19
    > 3
    > 15
    > 6
    > 7
    > 12
    > 14
    > 1
    > 1234567890
    > 1
    > 2
    > 3
    > 4
    > 5
    > 6
    > 7
    > 8
    > 9
    > 10
    > 11
    > 12
    > 13
    > 14
    > 15
    > 16
    > 17
    > 18
    > 19
    > 20
    > 21
    > 22
    """
    tab = [0 for _ in range(23)]
    n = 23
    m = n - 1
    q = 5
    w = 1
    for i in range(1, m + 1):
        w = w * q
        w = w % n
        tab[i] = w
    for i in range(1, m + 1):
        print(tab[i])
    print(1234567890)
    for i in range(2, m + 1):
        x = tab[i]
        j = i
        while j > 1:
            k = j - 1
            if tab[k] > x:
                tab[j] = tab[k]
                j = j - 1
            else:
                k = j
                j = 0
        tab[k] = x
    for i in range(1, m + 1):
        print(tab[i])

sort9()