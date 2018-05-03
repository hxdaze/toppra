import numpy as np
import pytest
import openravepy as orpy
import toppra
import matplotlib.pyplot as plt


@pytest.fixture(scope='module')
def env():
    env = orpy.Environment()
    env.Load('data/lab1.env.xml')
    env.GetRobots()[0].SetActiveDOFs(range(7))
    yield env
    env.Destroy()


# data for testing
string_cubic = '<trajectory>\n<configuration>\n<group name="deltatime" offset="21" dof="1" interpolation=""/>\n<group name="joint_accelerations BarrettWAM 0 1 2 3 4 5 6" offset="14" dof="7" interpolation="linear"/>\n<group name="joint_velocities BarrettWAM 0 1 2 3 4 5 6" offset="7" dof="7" interpolation="quadratic"/>\n<group name="joint_values BarrettWAM 0 1 2 3 4 5 6" offset="0" dof="7" interpolation="cubic"/>\n</configuration>\n<data count="3">\n1.911071950502442 -0.6139332280691878 0.3017613818592927 -0.03256939324749446 0.2539537657593125 1.631888814889273 -0.382110349743038 -1.779775794213163 1.920706198747754 -1.455710832072421 -0.3193021310659508 -0.07690742449115055 -0.2637324281121458 1.347565186712714 0.4776605898376532 -0.8504422050805607 0.5608265061401856 0.1473621703181671 0.02349624187884241 -0.07984377332949627 -0.4609439978291262 0 -1.0456781917878 1.530200377923445 -1.584932866633682 -0.3703179386680995 0.1351109604028186 0.7230459529542326 1.546352623822729 -0.5856243196190303 -0.2053993139536471 -0.05364456672195834 0.04910329472946667 -0.01816681979404454 -0.4633418614358862 0.1952051921398993 0.4776605898376537 -0.8504422050805603 0.5608265061401851 0.1473621703181669 0.0234962418788424 -0.07984377332949606 -0.4609439978291258 2.5 -1.017049647592708 -1.640929797837422 0.03353854824950098 0.2129470803998386 0.1631196667890898 -0.684820492290158 0.5939156109564592 0.6085271549751042 -2.331504826655046 1.348421698628505 0.4175087205248837 0.04057378490306146 -0.6629512947596263 -0.9571548024329148 0.4776605898376538 -0.8504422050805592 0.5608265061401851 0.1473621703181668 0.0234962418788424 -0.07984377332949606 -0.4609439978291255 2.5 </data>\n</trajectory>\n'
string_cubic_5wp = '<trajectory>\n<configuration>\n<group name="deltatime" offset="21" dof="1" interpolation=""/>\n<group name="joint_accelerations BarrettWAM 0 1 2 3 4 5 6" offset="14" dof="7" interpolation="linear"/>\n<group name="joint_velocities BarrettWAM 0 1 2 3 4 5 6" offset="7" dof="7" interpolation="quadratic"/>\n<group name="joint_values BarrettWAM 0 1 2 3 4 5 6" offset="0" dof="7" interpolation="cubic"/>\n</configuration>\n<data count="5">\n-0.1249152133150525 1.261299270966499 1.046319531681505 0.8782345303719905 -0.2466250993599075 -0.6003650091751073 -0.4132535904961724 -4.744914707961284 -1.246917392067082 2.520083613512308 -2.122153895258361 1.997918582410763 1.955728428656132 0.9029751714562115 8.609503476444049 0.5851410583399052 -6.503698111943587 0.6505337111557972 -3.468290122426431 -3.426963753875619 0.4517311358660031 0 -1.047696442944568 0.1549841504413256 0.5973926503361995 -1.141322803305591 0.2645225049283789 -0.1000255428267005 0.7457984214891809 1.8942147920342 -0.5270346665886928 -2.052780422288607 -1.009213379781847 -0.6014015880131204 -0.5687897919038265 0.6934425259361725 2.013103723548726 0.5666713024255177 -0.8128843453378751 1.130171113606625 -0.6906221502517838 -0.6122653990203157 -0.7869833686980656 1.25 1.174996895470801 -0.0659070600439767 -1.121666020599537 -1.394987771972822 -0.3034270005517463 -0.5563507624475375 0.675188919883807 0.2878446009105315 0.1697608639967116 0.4878727501676174 0.7032738887581991 0.2713632067813052 0.4250649311053417 -1.064483250288951 -4.583296029346595 0.5482015465111292 4.877929421267835 1.609808516057449 2.087045821922864 2.202432955834985 -2.025697873262133 1.25 -0.5075414623221984 0.3586312565370787 1.422188601664825 0.2608105387177909 0.8623903996545434 0.9724093452433777 -1.343055970486779 -1.749221242182639 0.336744265231654 2.080799704806838 1.561237845605167 0.950831708230695 1.442373798850647 -1.44876006552267 1.323990680397523 -0.2810281045352209 -2.329246293845082 -0.2370661851023002 -0.9998962196038397 -0.5747387674424961 1.410854968888182 1.25 -0.1213443819940674 0.344063159781851 0.3265958897962453 1.54619293518606 0.4658699567298331 1.603140128805392 -1.15683997196958 3.59782130190434 -0.5328093973413413 -5.335242984445088 0.1106084260024505 -2.228377342228295 -1.0117819875009 2.462654171931504 7.231277390141642 -1.110257755581571 -9.536422008957999 -2.083940886262045 -4.086838261130543 -3.35191049071998 4.847407811038496 1.25 </data>\n</trajectory>\n'
string_quad_4wp = '<trajectory>\n<configuration>\n<group name="deltatime" offset="14" dof="1" interpolation=""/>\n<group name="joint_velocities BarrettWAM 0 1 2 3 4 5 6" offset="7" dof="7" interpolation="linear"/>\n<group name="joint_values BarrettWAM 0 1 2 3 4 5 6" offset="0" dof="7" interpolation="quadratic"/>\n<group name="iswaypoint" offset="15" dof="1" interpolation="next"/>\n</configuration>\n<data count="4">\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.02116582932462694 0.01704773502820265 0.007755406269925299 0.004425403528166656 -0.02650172273501717 -0.00966003866448188 0.01460828601285267 -1.300164299367702 1.0472 0.4763953353586362 0.2718415418253199 -1.627934972135471 -0.5933921704384888 0.8973507088977886 0.03255869944270942 0 -1.203113132548262 0.9690314316561811 0.4408346579993372 0.2515498457396996 -1.506417261928573 -0.549098228087832 0.8303676873003374 -1.300164299367701 1.047199999999999 0.4763953353586358 0.2718415418253197 -1.62793497213547 -0.5933921704384884 0.8973507088977878 0.9090753405538373 0 -1.224278961872889 0.9860791666843838 0.4485900642692625 0.2559752492678663 -1.53291898466359 -0.5587582667523139 0.8449759733131901 0 0 0 0 0 0 0 0.03255869944270939 1 </data>\n</trajectory>\n'
string_quad_1wp = '<trajectory>\n<configuration>\n<group name="deltatime" offset="14" dof="1" interpolation=""/>\n<group name="joint_velocities BarrettWAM 0 1 2 3 4 5 6" offset="7" dof="7" interpolation="linear"/>\n<group name="joint_values BarrettWAM 0 1 2 3 4 5 6" offset="0" dof="7" interpolation="quadratic"/>\n</configuration>\n<data count="1">\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 1.264808053353591e-321 </data>\n</trajectory>\n'
string_quad_2wp = '<trajectory>\n<configuration>\n<group name="deltatime" offset="14" dof="1" interpolation=""/>\n<group name="joint_velocities BarrettWAM 0 1 2 3 4 5 6" offset="7" dof="7" interpolation="linear"/>\n<group name="joint_values BarrettWAM 0 1 2 3 4 5 6" offset="0" dof="7" interpolation="quadratic"/>\n<group name="iswaypoint" offset="15" dof="1" interpolation="next"/>\n</configuration>\n<data count="2">\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.0246741264 0 0 0 0 0 0 1.5708 0 0 0 0 0 0 0.031416 0 </data>\n</trajectory>\n'
string_quad_24wp = '<trajectory>\n<configuration>\n<group name="deltatime" offset="14" dof="1" interpolation=""/>\n<group name="joint_velocities BarrettWAM 0 1 2 3 4 5 6" offset="7" dof="7" interpolation="linear"/>\n<group name="joint_values BarrettWAM 0 1 2 3 4 5 6" offset="0" dof="7" interpolation="quadratic"/>\n<group name="iswaypoint" offset="15" dof="1" interpolation="next"/>\n</configuration>\n<data count="24">\n-1.22427896 0.9860791699999998 0.4485900600000001 0.2559752500000001 -1.53291898 0 0.5587582699999999 0 0 0 0 0 0 0 0 1 -1.1996048336 0.9785330977206376 0.4451571784225873 0.2540163730690252 -1.521188159825098 0.009183123435448649 0.5521865340044813 1.5708 -0.4803967582991 -0.2185435177879276 -0.1247056869731885 0.7468054605870661 0.5846144280270339 -0.4183687290246135 0.031416 0 -0.9604694103926973 0.9053984643470243 0.4118865541448762 0.2350314308544271 -1.407496003044469 0.09818364460895253 0.4884949226777673 1.5708 -0.4803967582991 -0.2185435177879276 -0.1247056869731885 0.7468054605870661 0.5846144280270339 -0.4183687290246135 0.1522379826886317 0 -0.9357952839926973 0.8978523920676621 0.4084536725674634 0.2330725539234522 -1.395765182869567 0.1073667680444012 0.4819231866822487 0 0 0 0 0 0 0 0.031416 1 -0.9111211575926973 0.8844019932095756 0.4043024017761823 0.2325020943062415 -1.388409461238424 0.1127092866962916 0.4810734092283289 1.5708 -0.8562769835807552 -0.2642774886224294 -0.03631650224157744 0.4682786880024844 0.3401145054679436 -0.05409838642219043 0.031416 0 -0.2337149983414925 0.5151332749114814 0.2903329603805406 0.2168406337123373 -1.186464676734378 0.2593833768762398 0.4577435262591772 1.5708 -0.8562769835807552 -0.2642774886224294 -0.03631650224157744 0.4682786880024844 0.3401145054679436 -0.05409838642219043 0.4312491464548032 1 0.422801383270808 0.2245820842405326 0.1727744309514951 0.1662157880318388 -0.8507760263582014 0.5147278521441822 0.3112893652751077 1.5708 -0.5340853077152686 -0.2982703569428146 -0.2059364249424625 1.138077975074019 0.8817745836233527 -0.6467224994445395 0.4179503320679274 1 0.7023859282851698 0.1417317721012366 0.1250771362105139 0.1231329884766986 -0.62282623631195 0.6922021803360373 0.1737201409112325 1.5708 -0.3968765256845076 -0.237688528590609 -0.2781708889130864 1.42331918789333 1.112446339492736 -0.8990978363660456 0.1779886331896879 1 0.7099288956647924 0.139834862582471 0.1239396823532999 0.121792535259064 -0.6160153170426177 0.6975590797972189 0.169386333139123 1.570800000000012 -0.3931747425011339 -0.2360540793221958 -0.2801197169693322 1.413387230105896 1.118669678947465 -0.9059067210764873 0.004801990947047776 1 0.7454979010636879 0.1311294950582019 0.118681763622079 0.1153454926041603 -0.5845410028947557 0.7224740813577541 0.1485095724860753 1.570799999999988 -0.3757189138588243 -0.2283468028716155 -0.2893094525422376 1.366552895236878 1.081925137375636 -0.9380141457592077 0.02264387916914655 1 0.7648271862684449 0.1265644970044717 0.1158976400022609 0.1118187928051495 -0.5678816485443317 0.7356647198400676 0.136859602314781 1.570800000000004 -0.3662328827895758 -0.2241584331661848 -0.2838871230789605 1.341101685513562 1.061957029867536 -0.9554623021505406 0.01230537637175778 1 1.563531391384623 0.03999904089954231 0.04591962479480991 0.02443357048486292 -0.1533427002493939 1.065868278096454 -0.1647584713233965 1.570799999999996 0.02573882359066604 -0.05109106616974268 -0.05983138082134104 0.2894338138881767 0.2368560876461854 -0.2309134976411573 0.5084697002267496 1 1.587325860518223 0.04038781174397496 0.04518474846468863 0.02357780091283479 -0.1491956563851189 1.069269997328558 -0.1680928607739504 1.570799999999992 0.02559085634511834 -0.04593515726673247 -0.05315645985660623 0.2581032179680687 0.2122752243227745 -0.20932821731554 0.01514799410084056 1 1.673334054300798 0.04921757762492762 0.03952056132800673 0.02027319827991446 -0.1287174430063588 1.089796867821935 -0.1959649666857494 1.570800000000003 0.2969318158752264 -0.1609592039098822 -0.06754994234766644 0.4898994120295795 0.5375046920537286 -0.8087492946232018 0.05475438870803031 1 1.688121610815132 0.0522324947915799 0.03791219936879484 0.01966574321075563 -0.1239179263546162 1.095120156209417 -0.2040636590644609 1.570799999999995 0.3435839962924608 -0.180735512601389 -0.0615032141639852 0.5297525837885115 0.593422028794434 -0.9118089296037692 0.009414028847934144 1 1.691519196433926 0.05298724718235178 0.03751636071747141 0.01953421640162527 -0.1227860452617904 1.096417601768504 -0.2060614783605907 1.570799999999987 0.3543027906461788 -0.185279312784872 -0.06011391927285624 0.5168487502741177 0.6062695833560446 -0.935487887878522 0.002162965125282528 1 1.693821864019443 0.05351195143242087 0.03724249886425007 0.01944678432539681 -0.1220347962221993 1.09729839902863 -0.2074445916453739 1.570799999999979 0.3615673081840051 -0.1883588117501562 -0.05917234349774984 0.5081033520718585 0.595429128961123 -0.9515359807878827 0.001465920286170689 1 1.69389681696708 0.053529209770426 0.03723350866513796 0.01944396156441086 -0.1220105581424766 1.097326802354514 -0.2074899812629825 1.570800000005942 0.3618037717565998 -0.188459050936239 -0.05914169474927243 0.5078186851157087 0.595076266901721 -0.9509378667987942 4.771641688121414e-05 1 1.694724793063355 0.05371913214146061 0.03713387917719905 0.01941287692743807 -0.1217437132841166 1.097639442555697 -0.2079894837767979 1.570799999994075 0.3588210428088179 -0.1895663542865124 -0.05880312993002576 0.504674079827697 0.5911783368937066 -0.944330733905572 0.0005271047213358677 1 1.763405240810972 0.06399901697656971 0.03107039636515491 0.01745577323407492 -0.1053802119616999 1.116419097840747 -0.2372971890819457 1.570800000005922 0.1114042870646194 -0.08779115031680756 -0.03071924746715657 0.2438297147808294 0.267845839249051 -0.3962704125079886 0.04372322876726339 1 1.787828466312236 0.0648882843054182 0.02951917070701802 0.01684428117181554 -0.1008727145016275 1.121034797676031 -0.243489982885057 0.158398516002219 -0.04844291673702948 -0.02203779532778911 -0.01257524557820131 0.07530740813785719 0.05895216313184587 -0.04218804801476422 0.02824802967983718 1 1.8122516918135 0.05741894488727754 0.02612119667036516 0.01490532324322101 -0.08926118014366094 1.130124541759935 -0.2499948936385871 1.5708 -0.4803967582991036 -0.2185435177879274 -0.1247056869731895 0.7468054605870724 0.584614428027033 -0.4183687290246126 0.02824802967983719 0 1.9753258736 0.00754607227936232 0.003432881577412763 0.001958876930974861 -0.01173082017490173 1.190816876564551 -0.2934282640044812 1.5708 -0.4803967582991036 -0.2185435177879274 -0.1247056869731895 0.7468054605870724 0.584614428027033 -0.4183687290246126 0.1038160057209701 0 2 0 0 0 0 1.2 -0.2999999999999999 0 0 0 0 0 0 0 0.031416 1 </data>\n</trajectory>\n'


@pytest.mark.parametrize("traj_string", [
    pytest.param(string_cubic, id="cubic 3wp", marks=[]),
    pytest.param(string_cubic_5wp, id="cubic 5wp", marks=[]),
    pytest.param(string_quad_1wp, id="quadratic 1wp", marks=[]),
    pytest.param(string_quad_2wp, id="quadratic 2wp"),
    pytest.param(string_quad_4wp, id="quadratic 4wp"),
    pytest.param(string_quad_24wp, id="quadratic 24wp"),
])
def test_consistency(request, env, traj_string):
    "Check the consistency between the OpenRAVE trajectory and the interpolator."
    robot = env.GetRobots()[0]
    active_indices = robot.GetActiveDOFIndices()
    traj = orpy.RaveCreateTrajectory(env, "")
    traj.deserialize(traj_string)
    path = toppra.RaveTrajectoryWrapper(traj, robot)
    spec = traj.GetConfigurationSpecification()

    N = 100
    ss = np.linspace(0, path.get_duration(), N)

    # Openrave samples
    qs_rave = []
    qds_rave = []
    qdds_rave = []
    for s in ss:
        data = traj.Sample(s)
        qs_rave.append(spec.ExtractJointValues(data, robot, active_indices, 0))
        qds_rave.append(spec.ExtractJointValues(data, robot, active_indices, 1))
        qdds_rave.append(spec.ExtractJointValues(data, robot, active_indices, 2))

    # Interpolator samples
    qs_ra = path.eval(ss)
    qds_ra = path.evald(ss)
    if path._interpolation != "quadratic":
        qdds_ra = path.evaldd(ss)
    plt.plot(qs_ra)
    plt.title(request.node.name)
    plt.show()

    np.testing.assert_allclose(qs_rave, qs_ra, atol=1e-8)
    np.testing.assert_allclose(qds_rave, qds_ra, atol=1e-8)
    if path._interpolation != "quadratic":
        np.testing.assert_allclose(qdds_rave, qdds_ra, atol=1e-8)

