# -----------
# User Instructions
#
# Write a function, doit, that takes as its input an
# initial robot position, move1, and move2. This
# function should compute the Omega and Xi matrices
# discussed in lecture and should RETURN the mu vector
# (which is the product of Omega.inverse() and Xi).
#
# Please enter your code at the bottom.

from math import *
import random


class matrix:
    def __init__(self, value=[[]]):
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if value == [[]]:
            self.dimx = 0

    def zero(self, dimx, dimy=0):
        if dimy == 0:
            dimy = dimx
        if dimx < 1 or dimy < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.dimx = dimx
            self.dimy = dimy
            self.value = [[0.0 for now in range(dimy)] for col in range(dimx)]

    def identity(self, dim):
        if dim < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.dimx = dim
            self.dimy = dim
            self.value = [[0.0 for now in range(dim)] for col in range(dim)]
            for i in range(dim):
                self.value[i][i] = 1.0

    def show(self, txt=''):
        for i in range(len(self.value)):
            print(txt + '[' + ', '.join('%.3f' %
                  x for x in self.value[i]) + ']')

        print(' ')

    def __add__(self, other):
        if self.dimx != other.dimx or self.dimx != other.dimx:
            raise ValueError("Matrices must be of equal dimension to add")
        else:
            res = matrix()
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res

    def __sub__(self, other):
        if self.dimx != other.dimx or self.dimx != other.dimx:
            raise ValueError("Matrices must be of equal dimension to subtract")
        else:
            res = matrix()
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res

    def __mul__(self, other):
        if self.dimy != other.dimx:
            raise ValueError("Matrices must be m*n and n*p to multiply")
        else:
            res = matrix()
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    for k in range(self.dimy):
                        res.value[i][j] += self.value[i][k] * other.value[k][j]
        return res

    def transpose(self):

        res = matrix()
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res

    def take(self, list1, list2=[]):
        if list2 == []:
            list2 = list1
        if len(list1) > self.dimx or len(list2) > self.dimy:
            raise ValueError("list invalid in take()")

        res = matrix()
        res.zero(len(list1), len(list2))
        for i in range(len(list1)):
            for j in range(len(list2)):
                res.value[i][j] = self.value[list1[i]][list2[j]]
        return res

    def expand(self, dimx, dimy, list1, list2=[]):
        if list2 == []:
            list2 = list1
        if len(list1) > self.dimx or len(list2) > self.dimy:
            raise ValueError("list invaild in expand()")

        res = matrix()
        res.zero(dimx, dimy)
        for i in range(len(list1)):
            for j in range(len(list2)):
                res.value[list1[i]][list2[j]] = self.value[i][j]
        return res

    def Cholesky(self, ztol=1.0e-5):
        res = matrix()
        res.zero(self.dimx, self.dimx)

        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError("Matrix not positive-definite")
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(i)])
                if abs(S) < ztol:
                    S = 0.0
                res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
        return res

    def CholeskyInverse(self):
        res = matrix()
        res.zero(self.dimx, self.dimx)

        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k]
                    for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0 / tjj**2 - S / tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum(
                    [self.value[i][k]*res.value[k][j] for k in range(i+1, self.dimx)])/self.value[i][i]
        return res

    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res

    def __repr__(self):
        return repr(self.value)


class robot:

    def __init__(self, world_size=100.0, measurement_range=30.0, motion_noise=1.0, measurement_noise=1.0):
        self.measurement_noise = 0.0
        self.world_size = world_size
        self.measurement_range = measurement_range
        self.x = world_size / 2.0
        self.y = world_size / 2.0
        self.motion_noise = motion_noise
        self.measurement_noise = measurement_noise
        self.landmarks = []
        self.num_landmarks = 0

    def rand(self):
        return random.random() * 2.0 - 1.0

    def make_landmarks(self, num_landmarks):
        self.landmarks = []
        for i in range(num_landmarks):
            self.landmarks.append(
                [round(random.random() * self.world_size), round(random.random() * self.world_size)])
            self.num_landmarks = num_landmarks

    def move(self, dx, dy):

        x = self.x + dx + self.rand() * self.motion_noise
        y = self.y + dy + self.rand() * self.motion_noise

        if x < 0.0 or x > self.world_size or y < 0.0 or y > self.world_size:
            return False
        else:
            self.x = x
            self.y = y
            return True

    def sense(self):
        Z = []
        for i in range(self.num_landmarks):
            dx = self.landmarks[i][0] - self.x + \
                self.rand() * self.measurement_noise
            dy = self.landmarks[i][1] - self.y + \
                self.rand() * self.measurement_noise
            if self.measurement_range < 0.0 or abs(dx) + abs(dy) <= self.measurement_range:
                Z.append([i, dx, dy])
        return Z

    def __repr__(self):
        return 'Robot: [x=%.5f y=%.5f]' % (self.x, self.y)


def make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance):
    complete = False

    while not complete:

        data = []

        r = robot(world_size, measurement_range,
                  motion_noise, measurement_noise)
        r.make_landmarks(num_landmarks)
        seen = [False for now in range(num_landmarks)]

        orientation = random.random() * 2.0 * pi
        dx = cos(orientation) * distance
        dy = sin(orientation) * distance

        for k in range(N-1):

            Z = r.sense()

            for i in range(len(Z)):
                seen[Z[i][0]] = True

            while not r.move(dx, dy):

                orientation = random.random() * 2.0 * pi
                dx = cos(orientation) * distance
                dy = sin(orientation) * distance

            data.append([Z, [dx, dy]])

        complete = (sum(seen) == num_landmarks)

    print(' ')
    print('Landmarks: ', r.landmarks)
    print(r)

    return data


def print_result(N, num_landmarks, result):
    print
    print('Estimated Pose(s):')
    for i in range(N):
        print(' [' + ', '.join('%.3f' % x for x in result.value[2*i]) +
              ', ' + ', '.join('%.3f' % x for x in result.value[2*i+1]) + ']')
    print
    print('Estimated Landmarks:')
    for i in range(num_landmarks):
        print(' [' + ', '.join('%.3f' % x for x in result.value[2*(N+i)]) +
              ', ' + ', '.join('%.3f' % x for x in result.value[2*(N+i)+1]) + ']')


def slam(data, N, num_landmarks, motion_noise, measurement_noise):
    #
    #
    #
    #
    # Add your code here!
    total = N + num_landmarks
    mtc = motion_noise  # motion confidence
    msc = measurement_noise  # measurement confidence
    omegax = [[0.0 for row in range(total)] for col in range(total)]
    xix = [[0.0 for row in range(1)] for col in range(total)]
    omegay = [[0.0 for row in range(total)] for col in range(total)]
    xiy = [[0.0 for row in range(1)] for col in range(total)]
    omegax[0][0] += 1.
    xix[0][0] += 50.
    omegay[0][0] += 1.
    xiy[0][0] += 50.
    for locI in range(len(data)):
        for measI in range(len(data[locI][0])):
            lmI = data[locI][0][measI][0] + N
            msx = data[locI][0][measI][1] * msc
            msy = data[locI][0][measI][2] * msc
            omegax[locI][locI] += msc
            omegax[lmI][lmI] += msc
            omegax[locI][lmI] += -msc
            omegax[lmI][locI] += -msc
            omegay[locI][locI] += msc
            omegay[lmI][lmI] += msc
            omegay[locI][lmI] += -msc
            omegay[lmI][locI] += -msc
            xix[locI][0] += -msx
            xix[lmI][0] += msx
            xiy[locI][0] += -msy
            xiy[lmI][0] += msy
        dx = data[locI][1][0] * mtc
        dy = data[locI][1][1] * mtc
        omegax[locI][locI] += mtc
        omegax[locI+1][locI+1] += mtc
        omegax[locI+1][locI] += -mtc
        omegax[locI][locI+1] += -mtc
        omegay[locI][locI] += mtc
        omegay[locI+1][locI+1] += mtc
        omegay[locI][locI+1] += -mtc
        omegay[locI+1][locI] += -mtc
        xix[locI][0] += -dx
        xix[locI+1][0] += dx
        xiy[locI][0] += -dy
        xiy[locI+1][0] += dy
    mux = matrix(omegax).inverse() * matrix(xix)
    muy = matrix(omegay).inverse() * matrix(xiy)
    mu = []
    for i in range(mux.dimx):
        mu.append(mux.value[i])
        mu.append(muy.value[i])
    mu = matrix(mu)
    return mu  # Make sure you return mu for grading!


num_landmarks = 5  # number of landmarks
N = 20  # time steps
world_size = 100.0  # size of world
measurement_range = 50.0  # range at which we can sense landmarks
motion_noise = 2.0  # noise in robot motion
measurement_noise = 2.0  # noise in the measurements
distance = 20.0

data = make_data(N, num_landmarks, world_size, measurement_range,
                 motion_noise, measurement_noise, distance)
result = slam(data, N, num_landmarks, motion_noise, measurement_noise)
print_result(N, num_landmarks, result)


test_data1 = [
    [
        [
            [1, 19.457599255548065, 23.8387362100849],
            [2, -13.195807561967236, 11.708840328458608],
            [3, -30.0954905279171, 15.387879242505843]
        ],
        [-12.2607279422326, -15.801093326936487]
    ],
    [
        [
            [2, -0.4659930049620491, 28.088559771215664],
            [4, -17.866382374890936, -16.384904503932]
        ],
        [-12.2607279422326, -15.801093326936487]
    ],
    [
        [
            [4, -6.202512900833806, -1.823403210274639]
        ],
        [-12.2607279422326, -15.801093326936487]
    ],
    [
        [
            [4, 7.412136480918645, 15.388585962142429]
        ],
        [14.008259661173426, 14.274756084260822]
    ],
    [
        [
            [4, -7.526138813444998, -0.4563942429717849]
        ],
        [14.008259661173426, 14.274756084260822]
    ],
    [
        [
            [2, -6.299793150150058, 29.047830407717623],
            [4, -21.93551130411791, -13.21956810989039]
        ],
        [14.008259661173426, 14.274756084260822]
    ],
    [
        [
            [1, 15.796300959032276, 30.65769689694247],
            [2, -18.64370821983482, 17.380022987031367]
        ],
        [14.008259661173426, 14.274756084260822]
    ],
    [
        [
            [1, 0.40311325410337906, 14.169429532679855],
            [2, -35.069349468466235, 2.4945558982439957]
        ],
        [14.008259661173426, 14.274756084260822]
    ],
    [
        [
            [1, -16.71340983241936, -2.777000269543834]
        ],
        [-11.006096015782283, 16.699276945166858]
    ],
    [
        [
            [1, -3.611096830835776, -17.954019226763958]
        ],
        [-19.693482634035977, 3.488085684573048]
    ],
    [
        [
            [1, 18.398273354362416, -22.705102332550947]
        ],
        [-19.693482634035977, 3.488085684573048]
    ],
    [
        [
            [2, 2.789312482883833, -39.73720193121324]
        ],
        [12.849049222879723, -15.326510824972983]
    ],
    [
        [
            [1, 21.26897046581808, -10.121029799040915],
            [2, -11.917698965880655, -23.17711662602097],
            [3, -31.81167947898398, -16.7985673023331]
        ],
        [12.849049222879723, -15.326510824972983]
    ],
    [
        [
            [1, 10.48157743234859, 5.692957082575485],
            [2, -22.31488473554935, -5.389184118551409],
            [3, -40.81803984305378, -2.4703329790238118]
        ],
        [12.849049222879723, -15.326510824972983]
    ],
    [
        [
            [0, 10.591050242096598, -39.2051798967113],
            [1, -3.5675572049297553, 22.849456408289125],
            [2, -38.39251065320351, 7.288990306029511]
        ],
        [12.849049222879723, -15.326510824972983]
    ],
    [
        [
            [0, -3.6225556479370766, -25.58006865235512]
        ],
        [-7.8874682868419965, -18.379005523261092]
    ],
    [
        [
            [0, 1.9784503557879374, -6.5025974151499]
        ],
        [-7.8874682868419965, -18.379005523261092]
    ],
    [
        [
            [0, 10.050665232782423, 11.026385307998742]
        ],
        [-17.82919359778298, 9.062000642947142]
    ],
    [
        [
            [0, 26.526838150174818, -0.22563393232425621],
            [4, -33.70303936886652, 2.880339841013677]
        ],
        [-17.82919359778298, 9.062000642947142]
    ]
]
test_data2 = [
    [
        [
            [0, 26.543274387283322, -6.262538160312672],
            [3, 9.937396825799755, -9.128540360867689]
        ],
        [18.92765331253674, -6.460955043986683]
    ],
    [
        [
            [0, 7.706544739722961, -3.758467215445748],
            [1, 17.03954411948937, 31.705489938553438],
            [3, -11.61731288777497, -6.64964096716416]
        ],
        [18.92765331253674, -6.460955043986683]
    ],
    [
        [
            [0, -12.35130507136378, 2.585119104239249],
            [1, -2.563534536165313, 38.22159657838369],
            [3, -26.961236804740935, -0.4802312626141525]
        ],
        [-11.167066095509824, 16.592065417497455]
    ],
    [
        [
            [0, 1.4138633151721272, -13.912454837810632],
            [1, 8.087721200818589, 20.51845934354381],
            [3, -17.091723454402302, -16.521500551709707],
            [4, -7.414211721400232, 38.09191602674439]
        ],
        [-11.167066095509824, 16.592065417497455]
    ],
    [
        [
            [0, 12.886743222179561, -28.703968411636318],
            [1, 21.660953298391387, 3.4912891084614914],
            [3, -6.401401414569506, -32.321583037341625],
            [4, 5.034079343639034, 23.102207946092893]
        ],
        [-11.167066095509824, 16.592065417497455]
    ],
    [
        [
            [1, 31.126317672358578, -10.036784369535214],
            [2, -38.70878528420893, 7.4987265861424595],
            [4, 17.977218575473767, 6.150889254289742]
        ],
        [-6.595520680493778, -18.88118393939265]
    ],
    [
        [
            [1, 41.82460922922086, 7.847527392202475],
            [3, 15.711709540417502, -30.34633659912818]
        ],
        [-6.595520680493778, -18.88118393939265]
    ],
    [
        [
            [0, 40.18454208294434, -6.710999804403755],
            [3, 23.019508919299156, -10.12110867290604]
        ],
        [-6.595520680493778, -18.88118393939265]
    ],
    [
        [
            [3, 27.18579315312821, 8.067219022708391]
        ],
        [-6.595520680493778, -18.88118393939265]
    ],
    [
        [],
        [11.492663265706092, 16.36822198838621]
    ],
    [
        [
            [3, 24.57154567653098, 13.461499960708197]
        ],
        [11.492663265706092, 16.36822198838621]
    ],
    [
        [
            [0, 31.61945290413707, 0.4272295085799329],
            [3, 16.97392299158991, -5.274596836133088]
        ],
        [11.492663265706092, 16.36822198838621]
    ],
    [
        [
            [0, 22.407381798735177, -18.03500068379259],
            [1, 29.642444125196995, 17.3794951934614],
            [3, 4.7969752441371645, -21.07505361639969],
            [4, 14.726069092569372, 32.75999422300078]
        ],
        [11.492663265706092, 16.36822198838621]
    ],
    [
        [
            [0, 10.705527984670137, -34.589764174299596],
            [1, 18.58772336795603, -0.20109708164787765],
            [3, -4.839806195049413, -39.92208742305105],
            [4, 4.18824810165454, 14.146847823548889]
        ],
        [11.492663265706092, 16.36822198838621]
    ],
    [
        [
            [1, 5.878492140223764, -19.955352450942357],
            [4, -7.059505455306587, -0.9740849280550585]
        ],
        [19.628527845173146, 3.83678180657467]
    ],
    [
        [
            [1, -11.150789592446378, -22.736641053247872],
            [4, -28.832815721158255, -3.9462962046291388]
        ],
        [-19.841703647091965, 2.5113335861604362]
    ],
    [
        [
            [1, 8.64427397916182, -20.286336970889053],
            [4, -5.036917727942285, -6.311739993868336]
        ],
        [-5.946642674882207, -19.09548221169787]
    ],
    [
        [
            [0, 7.151866679283043, -39.56103232616369],
            [1, 16.01535401373368, -3.780995345194027],
            [4, -3.04801331832137, 13.697362774960865]
        ],
        [-5.946642674882207, -19.09548221169787]
    ],
    [
        [
            [0, 12.872879480504395, -19.707592098123207],
            [1, 22.236710716903136, 16.331770792606406],
            [3, -4.841206109583004, -21.24604435851242],
            [4, 4.27111163223552, 32.25309748614184]
        ],
        [-5.946642674882207, -19.09548221169787]
    ]
]


### Uncomment the following three lines for test case 1 ###
result = slam(test_data1, 20, 5, 2.0, 2.0)
print_result(20, 5, result)
# print result
### Uncomment the following three lines for test case 2 ###
result = slam(test_data2, 20, 5, 2.0, 2.0)
print_result(20, 5, result)
