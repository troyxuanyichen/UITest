
import numpy as np
# import matplotlib.pyplot as plt # problem
from scipy import signal, fft,fftpack
import time
from CausalButter import CausalButter
from focus1desktop.PackageSender import PackageSender
import math
import random
import socket
import datetime


Alpha_Low = 8
Alpha_High = 12 #12
alphaWindow = signal.gaussian(Alpha_High - Alpha_Low + 1, std=7) # gaussian window for aipha wave
Beta_Low = 13
Beta_High = 18
betaWindow = signal.gaussian(Beta_High - Beta_Low + 1, std=7) # gaussian window for beta wave
Theta_Low = 4  #4
Theta_High = 8   #7
SampleRate = 160
Reward_Low = 12
Reward_High = 16
All_Low = 0.5
All_High = 79 ## Possible change to 20 or 19
First_Low = 3
First_High = 35
stamp = str(datetime.datetime.now())
newstamp = stamp.replace(':','_').replace('.','_').replace('-','_')
# old fengyin
eye_blink_pattern = [-1031.92184988534,-1367.43027000726,-1259.17692291247,-770.035094534798,-477.588314962962,-514.592756054578,-377.487440771104,176.491449581866,801.792675925146,1243.61162089452,1570.10358605718,1649.77320161167,1216.95678610377,563.958613323596,376.226900587245,708.667181543754,900.143139165632,710.381388151348,654.539478236346,960.745294498537,1169.87710534550,1065.48848539288,1087.59528672822,1475.75536391813,1770.49454915189,1551.03452397809,1048.40366885578,703.722008054725,635.892850857073,749.798030317055,892.385463824643,753.728710024545,137.143913120925,-501.189461018599,-414.524297249025,338.714753723255,858.960132374206,617.878077923323,-4.33266630524668,-513.864419481081,-889.444701005684,-1180.40727438588,-1258.72180992154,-1258.43311741977,-1674.03347412883,-2757.17085554830,-4180.67028999359,-5415.50701260745,-6117.28703301329,-6158.90429317981,-5768.78059064072,-5568.57972532731,-5896.73356119415,-6277.77935012071,-6094.26080228515,-5355.14784111230,-4160.83072928014,-1975.13605198608,1629.58966929830,5867.37152050699,9310.91117728788,11310.3294463145,12091.4250530580,11836.0791361553,10595.3463999638,8933.66181392401,7657.23583369333,6815.46750699836,5747.41092406556,4117.49081753595,2242.22998968661,503.339763892889,-883.542115006742,-1643.61187531193,-1738.04080663531,-1780.03630673968,-2418.91643656065,-3445.54890550693,-4154.52804496855,-4377.48127107035,-4471.79685960182,-4460.46145842398,-4001.74079219319,-3180.59321358707,-2541.86888218311,-2358.79763500580,-2492.99748178164,-2818.60202838584,-3188.33125891245,-3173.01509055016,-2497.09184164387,-1595.56060836291,-1079.08247256402,-837.104289852167,-359.215984175164,286.919437364104,587.592496315283,560.943604271677,751.787357910074,1238.65581419234,1446.38023124058,1054.99974054258,469.526049244715,243.306386830005,490.735797436570,995.338737070569,1487.12875643151,1743.43921494408,1807.42791093406,2038.13978496351,2560.03359792639,2849.19029278202,2327.74227270646,1243.93461257417,455.903422219142,389.204272999071,651.027862507558,585.852056528783,-74.6490324034899,-912.517903898903,-1083.86054151571,-267.431078481164,650.430807985615,492.225012212276,-558.045522189457]
eye_blink_norm = [0.28557891703396787, 0.26731419458012756, 0.2732073919510522, 0.29983575416215746, 0.31575624658812396, 0.3137417640727455, 0.3212056319830916, 0.351363655063128, 0.38540439044930913, 0.40945654509205015, 0.42723042130337713, 0.43156755065344865, 0.4080054841638949, 0.3724569563971085, 0.362237041118477, 0.3803347373311111, 0.390758485329078, 0.3804280569202435, 0.37738808258660617, 0.3940576023731682, 0.40544251628978695, 0.3997597105644309, 0.40096318137623777, 0.42209420418323207, 0.438139492741443, 0.42619232179397265, 0.3988296312772657, 0.3800655273326545, 0.37637297997410285, 0.382573857103015, 0.39033616571355634, 0.3827878391362711, 0.34922161692161047, 0.31447142523507976, 0.31918938480847187, 0.36019491963947065, 0.3885165261300013, 0.3753922748472857, 0.3415197820287672, 0.3137814139431215, 0.2933352218663645, 0.27749552805089106, 0.27323216781945353, 0.2732478839329789, 0.2506230414200858, 0.19165819146544988, 0.11416439243085696, 0.04694119127794384, 0.008737031478600523, 0.006471431986478882, 0.02770935247429168, 0.03860807519081641, 0.020743728501416297, 0.0, 0.009990555051137799, 0.05022708053968591, 0.11524443706850152, 0.23423133651831304, 0.4304687805668206, 0.6611691287253593, 0.8486317744230141, 0.9574779838255633, 1.0, 0.9860992391777996, 0.9185550653007427, 0.82809471930164, 0.7586074430857033, 0.7127824684042028, 0.6546386011201096, 0.5659074796869158, 0.46382026966464435, 0.3691569305440445, 0.2936565523861512, 0.2522791609857016, 0.2471385501431852, 0.24485235967011806, 0.2100724031843372, 0.15418362071923347, 0.11558754851596845, 0.10345021141588047, 0.09831577083471142, 0.09893285804921693, 0.12390512446655891, 0.168607527498452, 0.20337900248369586, 0.21334520696153544, 0.20603950967436185, 0.18831394358790382, 0.16818627652015483, 0.16902007247702489, 0.20581661706712834, 0.25489502098128775, 0.2830115427675832, 0.29618457832213235, 0.3222003106961652, 0.3573752375660223, 0.3737435599142209, 0.3722928225029156, 0.3826821539867208, 0.4091867562327503, 0.42049505312405683, 0.39918871442218723, 0.3673161477912366, 0.35500098936360414, 0.3684707839815871, 0.39594083268694524, 0.42271335960573975, 0.4366666290499089, 0.4401501057746225, 0.4527098154368181, 0.4811211609424824, 0.49686254464691726, 0.46847546763310133, 0.4094741284164316, 0.366574546428076, 0.36294351550500953, 0.3771969139517697, 0.3736488122186594, 0.33769183365632294, 0.29207914117899264, 0.28275142976285983, 0.327196983588439, 0.3771644109370044, 0.3685518552540831, 0.31137624158297666]
eye_blink_pattern = eye_blink_pattern[2:123]
replace_pattern = [0.486900000000000,0.873800000000000,-1.24900000000000,0.220200000000000,0.0370000000000000,-0.827300000000000,-0.188500000000000,0.764200000000000,2.86560000000000,2.40070000000000,0.224200000000000,2.27190000000000,1.08860000000000,0.413900000000000,0.688700000000000,0.176100000000000,0.312900000000000,1.31260000000000,1.40170000000000,1.30300000000000,0.652700000000000,-0.433500000000000,0.614300000000000,1.20930000000000,0.612300000000000,0.755500000000000,0.415200000000000,-0.303600000000000,-0.237200000000000,-0.837400000000000,-0.199900000000000,-1.40490000000000,-1.59170000000000,-1.62300000000000,-2.50680000000000,-0.0557000000000000,-0.387000000000000,-0.908400000000000,0.0440000000000000,-1.51690000000000,-0.786400000000000,-0.677200000000000,-0.321800000000000,-0.343500000000000,-0.954400000000000,-0.514400000000000,-0.399300000000000,0.153100000000000,0.518100000000000,0.367100000000000,-0.808500000000000,-0.590300000000000,-1.30180000000000,-1.23410000000000,-0.366000000000000,0.527300000000000,-0.554200000000000,-0.0500000000000000,-0.141600000000000,0.603200000000000,0.486900000000000,0.873800000000000,-1.24900000000000,0.220200000000000,0.0370000000000000,-0.827300000000000,-0.188500000000000,0.764200000000000,2.86560000000000,2.40070000000000,0.224200000000000,2.27190000000000,1.08860000000000,0.413900000000000,0.688700000000000,0.176100000000000,0.312900000000000,1.31260000000000,1.40170000000000,1.30300000000000,0.652700000000000,-0.433500000000000,0.614300000000000,1.20930000000000,0.612300000000000,0.755500000000000,0.415200000000000,-0.303600000000000,-0.237200000000000,-0.837400000000000,-0.199900000000000,-1.40490000000000,-1.59170000000000,-1.62300000000000,-2.50680000000000,-0.0557000000000000,-0.387000000000000,-0.908400000000000,0.0440000000000000,-1.51690000000000,-0.786400000000000,-0.677200000000000,-0.321800000000000,-0.343500000000000,-0.954400000000000,-0.514400000000000,-0.399300000000000,0.153100000000000,0.518100000000000,0.367100000000000,-0.808500000000000,-0.590300000000000,-1.30180000000000,-1.23410000000000,-0.366000000000000,0.527300000000000,-0.554200000000000,-0.0500000000000000,-0.141600000000000,0.603200000000000,-1.30180000000000]
rpLen = 30 # rpLen: replace pattern length must be an even number

class DataProcessor:

    def __init__(self):
        self.dataFromSocket = []
        self.maxPlotSize = 300
        self.maxRawDataSize = 3 * SampleRate #1120
        self.maxBufferSize = 0.5 * SampleRate
        self.fftWindowSize = self.maxRawDataSize
        self.FFT_N = 2**10
        self.count = 0
        self.Epre = 0.8  # if no pre accessment
        self.Emin, self.Emax = 0, 0.8
        self.engInd = self.Emin
        self.count = 0
        self.sock = None
        self.PackageSender = None
        self.rawdata_array = []
        self.firstFiltered_array = []
        self.rawfft_y = []
        self.rawfft_x = []
        self.bw_buffer = []
        self.engIndBuff = []
        self.scalEngIndBuff = []
        self.EminBuff = []
        self.EmaxBuff = []
        self.timerCount = 0
        self.engRawBuffer = []
        self.maxEngRaw = 4 * SampleRate
        self.attenIdx_buffer = []

        # eye blink detection variable
        self.blinkThresh = 5 # if larger than this threshhold, a peak may be considered as a blink
        self.signalThresh = 50 # if larger than this threshhold, a peak may not be considered as a blink
        self.displayFlag = 0 # default no output if no blink is detected
        self.lastFiftySamplePoints = [] # last 50 data points of a data series for next eye blink detection
        self.patternSegementIndex = [] # the index at the end of the data point that may count as part of a blink
        self.wearDetectionDataArray = [] # data points for eye detection
        self.wearDetectionFailCount = 0 # count the number of wear detection failure

        self.rawdatafile = open('focusOne_rawdata.txt', 'w')
        self.rawdataForEyeBlinkFile = open('rawdataForEyeBlink.txt','a')
        # self.rawdataWithTimeStamp = open('rawdata_' + newstamp + '.txt', 'a')
        self.indexfile = open('indexes.txt','w')
        self.freqfile = open('frequency_energy.txt','w')

        self.indexfile.writelines("betaPower    alphaPower    thetaPower    index0    index1    index2    index3    index4    index5    index6    index7    average\n")
        self.butter_dict = self.init_filter()
        self.causal_dict = self.initCausalBurtter()

        self.filtered_output_dict = {}
        self.filtered_output_dict['Alpha'] = []
        self.filtered_output_dict['Beta'] = []
        self.filtered_output_dict['Theta'] = []
        self.filtered_output_dict['Reward'] = []
        self.filtered_output_dict['All'] = []

        self.ratio_dict = {}
        self.ratio_dict['Alpha'] = []
        self.ratio_dict['Beta'] = []
        self.ratio_dict['Theta'] = []
        self.ratio_dict['Reward'] = []
        self.ratio_dict['Attention'] = []

        self.signal_array = []
        self.Eave = 0.0
        self.rawdata_array_noblink = []
        self.PGA = 128 #amplification
        self.alpha_array = []
        self.beta_array = []
        self.theta_array = []
        self.rawdata_array_whole = []

        self.histox = np.linspace(4, 20, num = 161)
        self.histoy = [0] * len(self.histox)
        self.casualStop = CausalButter(4, 59, 61, 160, bandstop=1)
        self.message = ''
        #init files
        # current_time = time.strftime("%d%m%Y") + "_" + time.strftime("%M")
        # self.fileName_dict = {}
        # self.fileName_dict['Alpha'] = current_time + 'Alpha.txt'
        # self.fileName_dict['Beta'] = current_time + 'Beta.txt'
        # self.fileName_dict['Theta'] = current_time + 'Theta.txt'
        # self.fileName_dict['Reward'] = current_time + 'Reward.txt'
        # self.fileName_dict['All'] = current_time + 'All.txt'
        # self.fileName_dict['Ratio'] = current_time + 'Ratio.txt'
        # self.rawfile = open('rawData.txt','w')
        # for k, v in self.fileName_dict.items():
        #     tempFile = open(v, 'w')
        #     tempFile.close()
        # tempFile = open(self.fileName_dict['Ratio'],'a')
        # tempFile.write("Alpha" + "    " + "Beta" + "    " + "Theta" + "    " +  "Attention" + "\n")
        # tempFile.close()

    def setSocket(self, sock):
        self.sock = sock
        self.PackageSender = PackageSender(self.sock)

    def filter_data(self, data, key):
        return signal.lfilter(self.butter_dict[key][0],self.butter_dict[key][1], data)

    def init_filter(self):
        filter_dict = {}
        Alpha_b, Alpha_a = self.butter_bandpass(Alpha_Low, Alpha_High)
        Beta_b, Beta_a = self.butter_bandpass(Beta_Low, Beta_High)
        Theta_b, Theta_a = self.butter_bandpass(Theta_Low, Theta_High)
        Reward_b, Reward_a = self.butter_bandpass(Reward_Low, Reward_High)
        All_b, All_a = self.butter_bandpass(All_Low, All_High)
        First_b, First_a = self.butter_bandpass(First_Low, First_High)
        filter_dict['Alpha'] = [Alpha_b, Alpha_a]
        filter_dict['Beta'] = [Beta_b, Beta_a]
        filter_dict['Theta'] = [Theta_b, Theta_a]
        filter_dict['Reward'] = [Reward_b, Reward_a]
        filter_dict['All'] =[All_b, All_a]
        filter_dict['First'] = [First_b, First_a]
        return filter_dict

    def butter_bandpass(self, lowcut, highcut):
        order = 4
        nyq = 0.5 * SampleRate
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='bandpass') #bandpass, range:0.5~30, pandstop: 60Hz
        return b, a

    def prepareDataForPlotting(self):
        dataSize = len(self.scalEngIndBuff)
        if dataSize > self.maxPlotSize:
            self.scalEngIndBuff = self.scalEngIndBuff[(dataSize - self.maxPlotSize) : dataSize]
            self.EmaxBuff = self.EmaxBuff[(dataSize - self.maxPlotSize) : dataSize]
            self.EminBuff = self.EminBuff[(dataSize - self.maxPlotSize) : dataSize]
            self.engIndBuff = self.engIndBuff[(dataSize - self.maxPlotSize) : dataSize]
            self.alpha_array = self.alpha_array[(dataSize - self.maxPlotSize) : dataSize]
            self.beta_array = self.beta_array[(dataSize - self.maxPlotSize) : dataSize]
            self.theta_array = self.theta_array[(dataSize - self.maxPlotSize) : dataSize]
        rawdataSize = len(self.rawdata_array_whole)
        if rawdataSize > self.maxRawDataSize:
            # self.rawdata_array = self.rawdata_array[(rawdataSize - self.maxRawDataSize) : rawdataSize]            # self.rawdata_array = signal.detrend(self.rawdata_array).tolist()
            self.rawdata_array_noblink = self.rawdata_array_noblink[(rawdataSize - self.maxRawDataSize) : rawdataSize]
            self.rawdata_array_whole = self.rawdata_array_whole[(rawdataSize - self.maxRawDataSize) : rawdataSize]
        #remove data from index buffer

    # def wearDetection(self, rawdata):

    def blinkDetection(self):
        data = self.wearDetectionDataArray # may be empty, error handling
        pattern = eye_blink_norm
        blinkthresh = self.blinkThresh
        signalthresh = self.signalThresh
        lastepc = self.lastFiftySamplePoints
        cross_idx = [x for x, i in enumerate(data) if ((abs(i)>blinkthresh) & (abs(i)<signalthresh))]
        cross_count = len(cross_idx)
        pattern_half = len(pattern)/2
        whetherBlink = 0
        latepeak_idx = self.patternSegementIndex
        if cross_count >= 1: # pass the blink threshold
            cross_diff = [cross_idx[i]-cross_idx[i-1] for i in range(1,cross_count)] # continuous
            idx_start = [0]+[x+1 for x, i in enumerate(cross_diff) if i>1] #
            idx_end = [x for x, i in enumerate(cross_diff) if i>1] + [len(cross_diff)]
            num_list = [cross_idx[:idx_end[0]+1]] + [cross_idx[idx_start[i]:(idx_end[i]+1)] for i in range(1,len(idx_start)-1)] + [cross_idx[idx_start[-1]:]]
            peak_idx = [np.argmax(data[i])+i[0] for i in num_list if len(i)>1]
            earlypeak_idx = [t for t in peak_idx if t < pattern_half]
            if len(lastepc) != 0:
                new_data = lastepc.extend(data[:len(pattern)])
            else:
                new_data = data[:len(pattern)]
            # index of peak
            if len(earlypeak_idx) != 0: # peak detected
                if len(latepeak_idx) != 0: # last segement peak detected
                    if lastepc[latepeak_idx[0]] >= data[earlypeak_idx[0]]:
                        peak = latepeak_idx[0]
                    else:
                        peak = earlypeak_idx[0] + len(lastepc)
                else:
                    peak = earlypeak_idx[0] + len(lastepc)
            else:
                if len(latepeak_idx) != 0:
                    peak = latepeak_idx[0]
                else:
                    peak = None
            if peak != None:
                event_cur = new_data[peak-pattern_half:peak-pattern_half] # new_data may be empty
                event_curnorm = [(i-min(event_cur))/(max(event_cur)-min(event_cur)) for i in event_cur]
            else:
                event_curnorm = []
            self.patternSegementIndex = [t-len(data)+len(lastepc) for t in peak_idx if t > (len(data)-pattern_half)]
            event_trace = [data[t-pattern_half:t+pattern_half] for t in peak_idx if (t >= pattern_half & t <= (len(data)-pattern_half))]
            event_normtrace = []
            for event in event_trace:
                event_normtrace.append([(i-min(event))/(max(event)-min(event)) for i in event])
            event_normtrace = event_curnorm + event_normtrace
            if event_normtrace is not []:
                event_corr = [np.correlate(i,pattern)[0] for i in event_normtrace]
                print 'salt'
                print "event_corr is : "+str(event_corr)
                blink_count = [i for i, x in enumerate(event_corr) if x > 0.8]
            else:
                blink_count = []
            if blink_count is not []:
                whetherBlink = 1
        else:
            self.patternSegementIndex = []
        return whetherBlink

    # receive rawdata from PackageReceiver and analyse it using FFT, the rawdata contain the data in 3 seconds
    def processRawDataWithFFT(self, rawdata):
        rawdata = [i*0.0019*128/self.PGA  for i in rawdata] #i is data point in a package, conversion according to hardware
        self.rawdatafile.write(str(rawdata)+'\n')
        print 'Sample rate is : ' + str(len(rawdata) * 2)
        ## wear detection
        # overCount = 0 #overflow count
        # maxValue = 8388607*0.0019*128/self.PGA  # max range
        # # minValue = 83*0.0019*128/self.PGA
        # for i in rawdata:
        #     if i >= maxValue - 10: # 10 for allowance
        #         overCount += 1
        # if self.PGA < 16 or (1.0 * overCount / len(rawdata) > 0.9):
        #     print 'Please wear your FocusOne'
        #     self.message = 'Please wear your FocusOne'
        #     rawdata = [0] * len(rawdata)
        #     if self.sock: #send data to PCB
        #         self.PackageSender.sendData({'color': 'off'}) # turn off light if not properly weared, force light color when wear detection
        #         # did not pass
        #         scalEngInd = 0
        #         self.scalEngIndBuff.append(scalEngInd)
        #     return

        self.rawdata_array.extend(rawdata) # accumulate 3 seconds for FFT
        maxDataSize = 3 * SampleRate
        if len(self.rawdata_array) >= maxDataSize:
            the_rawdata_array = [i for i in self.rawdata_array]
            tempDict = self.causalFilData(the_rawdata_array)
            the_rawdata_array = tempDict['All']
            b, a = signal.butter(4, [59/(0.5*SampleRate), 61/(0.5 * SampleRate)], 'bandstop')
            the_rawdata_array = signal.filtfilt(b,a,the_rawdata_array)
            b, a = signal.butter(4, [3/(0.5*SampleRate), 35/(0.5 * SampleRate)], 'band')
            the_rawdata_array = signal.filtfilt(b,a,the_rawdata_array)
            print '#########'
            print 'the_rawdata_array'
            print self.rawdata_array
            print '##########'
            ################################
            # wear detection
            # eye link pattern collect
            # 1
            # print '#########'
            # print 'self.lastFiftySamplePoints'
            # print self.lastFiftySamplePoints
            # print '##########'
            # end wear detection
            ###################################
            self.rawdata_array_whole.extend(the_rawdata_array[int(2.5 * SampleRate):])

            # write to multiple file

            # self.rawdataWithTimeStamp.write(str(the_rawdata_array[:int(0.5 * SampleRate)]))
            # end write to multiple file

            self.signal_array = the_rawdata_array
            self.rawdata_array = self.rawdata_array[int(0.5 * SampleRate):]
            # if use PSD, uncomment line#211, commone line #212, #213
            # sig_freq, sig_fft = signal.welch(self.signal_array, SampleRate, nperseg=SampleRate/2, noverlap=SampleRate*0.4)
            sig_freq = fftpack.fftfreq(len(self.signal_array), d=1.0/SampleRate )
            sig_fft = fftpack.fft(self.signal_array)
            if self.count == 0:
                self.freqfile.writelines("%0.2f    " % i for i in sig_freq[0:240])
                self.freqfile.writelines("\n")
            self.freqfile.writelines("%0.2f    " % abs(i) for i in sig_fft[0:240])
            self.freqfile.writelines("\n")
            alphaPower = 0.0
            betaPower = 0.0
            thetaPower = 0.0
            alpha_count = 0.0
            beta_count = 0.0
            theta_count = 0.0
            otherPower = 0.0
            other_count = 0
            ######################
            # alpha range 8 - 12
            # beta range 13 - 18

            ######################
            for i in range(0, len(sig_freq)):
                if sig_freq[i] >= Alpha_Low and sig_freq[i] <= Alpha_High: #calculate alpha wave energy
                    alpha_count += 1
                    alphaPower += abs(sig_fft[i])
                if sig_freq[i] >= Beta_Low and sig_freq[i] <= Beta_High:
                    beta_count += 1
                    betaPower += abs(sig_fft[i])
                if sig_freq[i] >= Theta_Low and sig_freq[i] <= Theta_High:
                    theta_count += 1
                    thetaPower += abs(sig_fft[i])
                if sig_freq[i] >= 6 and sig_freq[i] <= 7: #special test for Max
                    other_count += 1
                    otherPower += abs(sig_fft[i])

            self.histoy = [0] * len(self.histox)
            for i in range(0, len(sig_freq)):
                if sig_freq[i] >= 4.0 and sig_freq[i] <= 8.0:
                    self.histoy[0:40] = [item + abs(sig_fft[i])  for item in self.histoy[0:40] ]
                if sig_freq[i] >= 8.0 and sig_freq[i] <= 12.0:
                    self.histoy[40:80] = [item + abs(sig_fft[i])  for item in self.histoy[40:80] ]
                if sig_freq[i] >= 12.0 and sig_freq[i] <= 16.0:
                    self.histoy[80:120] = [item + abs(sig_fft[i])  for item in self.histoy[80:120] ]
                if sig_freq[i] >= 16.0 and sig_freq[i] <= 20.0:
                    self.histoy[120:] = [item + abs(sig_fft[i])  for item in self.histoy[120:] ]

            self.beta_array.append(betaPower) #beta power array
            self.alpha_array.append(alphaPower)
            self.theta_array.append(thetaPower)
            if (alphaPower + thetaPower) != 0:
                self.engInd = (1.0 * betaPower/beta_count)/(1.0 * alphaPower/alpha_count + 0.0 * thetaPower/theta_count)
            else:
                self.scalEngInd = 0
                self.message = 'Please wear your FocusOne'
                print 'Please check device connection.'
                return
            self.engRawBuffer.append(self.engInd)

            #perform N point smoothing
            smoothPoint = 5
            if len(self.engRawBuffer) >= smoothPoint:
                self.indexfile.writelines("%0.2f    %0.2f    %0.2f    " % (betaPower, alphaPower, thetaPower))
                self.indexfile.writelines("%0.2f    " % i for i in self.engRawBuffer)
                self.engInd = sum(self.engRawBuffer)/smoothPoint
                self.indexfile.writelines("%0.2f\n" % self.engInd)
                self.engRawBuffer = self.engRawBuffer[1:smoothPoint]

            if self.count < 10000:
                self.Eave = (self.Eave * self.count) * self.engInd / (self.count + 1)
                self.count += 1

            if self.engInd > 1.3 * self.Emax and len(self.scalEngIndBuff) != 0: #noise canceling
                scalEngInd = np.mean(self.scalEngIndBuff)+2*np.std(self.scalEngIndBuff)
            else:
#                self.updateLimit(self.engInd)
                scalEngInd = (self.engInd - self.Emin)/(self.Emax - self.Emin) * 100
            self.attenIdx_buffer.append(scalEngInd)

            #reduce changes
            buffer_Len = 10
            std_folders = 1.5
            if len(self.attenIdx_buffer)>= 10:
                buffer_mean = np.mean(self.attenIdx_buffer)
                buffer_std = np.std(self.attenIdx_buffer)
                self.attenIdx_buffer = self.attenIdx_buffer[1:]
                if len(self.scalEngIndBuff) >4 and scalEngInd > (buffer_mean+std_folders*buffer_std):
                    scalEngInd = buffer_mean+std_folders*buffer_std
                    if  len(self.scalEngIndBuff) >4 and scalEngInd < (buffer_mean-std_folders*buffer_std):
                        scalEngInd = buffer_mean-std_folders*buffer_std
            if scalEngInd > 95:
                scalEngInd = 95 + np.random.rand()*5

            self.engIndBuff.append(self.engInd)
            self.EmaxBuff.append(self.Emax)
            self.EminBuff.append(self.Emin)
            self.scalEngIndBuff.append(scalEngInd)

            pidxs = np.where(sig_freq > 0)
            self.rawfft_x = sig_freq[pidxs]
            self.rawfft_y = np.abs(sig_fft)[pidxs]

            self.prepareDataForPlotting()

            self.signal_array = self.signal_array[int(0.5*SampleRate):]
            if self.sock:
                self.timerCount += 1
                if self.timerCount == 4:
                    self.timerCount = 0
                    if scalEngInd >= 0 and scalEngInd < 30:
                        lightColor = 'blue'
                        self.message = 'Connected:  Not Focused'
                    elif scalEngInd >= 30 and scalEngInd < 70:
                        lightColor = 'green'
                        self.message = 'Connected:  Focused'
                    else:
                        lightColor = 'red'
                        self.message = 'Connected:  Highly Focused'
                    print lightColor
                    # lightColor = 'red' # force red color
                    self.PackageSender.sendData({'color': lightColor})
            else:
                self.message = 'Connected'

    def changeParameter(self, newSampleRate, newPGA):
        SampleRate = newSampleRate
        self.PGA = newPGA

    # receive rawdata from PackageReceiver and analyse it using three filters
    def processRawData(self, rawdata80):
        rawdata = [i*0.0019*128/self.PGA for i in rawdata80]
        for one in rawdata:
            self.rawdatafile.write(str(one)+'\n')
        self.rawdata_array.extend(rawdata)  #rawdata_array is for fft
        tempDict = self.causalFilData(rawdata)
        for k, v in tempDict.items():
            self.filtered_output_dict[k].extend(v)

        self.betaFiltered_array = self.filtered_output_dict['Beta']
        self.alphaFiltered_array = self.filtered_output_dict['Alpha']
        self.thetaFiltered_array = self.filtered_output_dict['Theta']

        self.firstFiltered_array.extend(tempDict['First'])
        if len(self.betaFiltered_array) >= 0.5 * SampleRate:
            # print len(self.betaFiltered_array)
            self.engInd = self.calculateEngagement(self.filtered_output_dict)
            self.engRawBuffer.append(self.engInd)
            if len(self.engRawBuffer) >= 3:
                # print self.engRawBuffer
                self.engInd = sum(self.engRawBuffer)/3
                # print self.engInd
                self.engRawBuffer = self.engRawBuffer[1:3]
            scalEngInd = (self.engInd - self.Emin)/(self.Emax - self.Emin) * 100
            if self.count < 0:
                self.count += 1
                if self.engInd > self.Epre:
                    self.Epre = self.engInd
                    self.Emax = self.Epre
                    scalEngInd = (self.engInd - self.Emin)/(self.Emax - self.Emin) * 100
                if self.engInd < self.Emin:
                    self.Emin = self.engInd
            else:
                if self.engInd > 1.3 * self.Emax and len(self.scalEngIndBuff) != 0:
                    scalEngInd = self.scalEngIndBuff[len(self.scalEngIndBuff) - 1]
                else:
                    self.updateLimit(self.engInd)
            self.engIndBuff.append(self.engInd)
            self.EmaxBuff.append(self.Emax)
            self.EminBuff.append(self.Emin)
            self.scalEngIndBuff.append(scalEngInd)

            self.prepareDataForPlotting()
            for k, v in self.filtered_output_dict.items():
                self.filtered_output_dict[k] = []
        self.rawfft_y = self.performFFT()

        if len(self.rawfft_y) != 0:
            self.rawfft_x = []
            for i in range (0, len(self.rawfft_y)):
                self.rawfft_x.append(0.5 * i * SampleRate/len(self.rawfft_y))
        if self.sock:
            self.timerCount += 1
            if self.timerCount == 4:
                self.timerCount = 0
                print scalEngInd #scaled attention level
                if scalEngInd >= 0 and scalEngInd < 30:
                    lightColor = 'blue'
                elif scalEngInd >= 30 and scalEngInd < 70:
                    lightColor = 'green'
                else:
                    lightColor = 'red'
                print lightColor
                self.PackageSender.sendData({'color': lightColor})


    def updateLimit(self, engInd):
        if engInd < self.Emin:
            self.Emin = engInd
        if engInd > self.Emax:
            self.Emax = engInd
        elif self.Emax > self.Epre: #avoid noise to pull up the upper bound
            self.Emax -= 0.001 * (self.Emax - 2 * self.Eave) #slope

    def performFFT(self):
        data_freqDomain = []
        rawdataSize = len(self.firstFiltered_array)
        if rawdataSize >= self.fftWindowSize - 1:
            fftBuffer = self.firstFiltered_array[(rawdataSize - self.fftWindowSize) : rawdataSize]
            data_freqDomain = abs(fft(fftBuffer,self.FFT_N)[:self.FFT_N/2])
        return data_freqDomain


    def calculate_index(self,key1, key2):
        numerator = [i*i for i in self.filtered_output_dict[key1]]
        denominator = [i*i for i in self.filtered_output_dict[key2]]
        return sum(numerator)/sum(denominator)


    def writeToFile(self, key, data):
        tempFile = open(self.fileName_dict[key], 'a')
        for singleData in data:
            tempFile.write(str(singleData) + '\n')
        tempFile.close()

    def initCausalBurtter(self):
        causal_dict = {}
        filter_order = 4
        causal_dict['First'] = CausalButter(filter_order, First_Low, First_High, SampleRate)
        causal_dict['Alpha'] = CausalButter(filter_order, Alpha_Low, Alpha_High, SampleRate)
        causal_dict['Beta'] = CausalButter(filter_order, Beta_Low, Beta_High, SampleRate)
        causal_dict['Theta'] = CausalButter(filter_order, Theta_Low, Theta_High, SampleRate)
        causal_dict['Reward'] = CausalButter(filter_order, Reward_Low, Reward_High, SampleRate)
        causal_dict['All'] = CausalButter(filter_order, All_Low, All_High, SampleRate)
        return causal_dict

    def causalFilData(self, data):
        dataDict = {}
        dataDict['First'] = []
        dataDict['Alpha'] = []
        dataDict['Beta'] = []
        dataDict['Theta'] = []
        dataDict['All'] = []
        dataDict['Reward'] = []
        for onedata in data:
            for k, v in self.causal_dict.items():
                dataDict[k].extend(v.inputData([onedata]))
        return dataDict



    def calculateEngagement(self, dataDict):
        numerator = [i*i for i in dataDict['Beta']]
        denominator1 = [i*i for i in dataDict['Alpha']]
        denominator2 = [i*i for i in dataDict['Theta']]
        return sum(numerator)/(sum(denominator1) + sum(denominator2))

    def pattern_det(self, data, pattern):
# Find a pattern in a data sequence and output the
# index of the detected pattern centre point
        patternPower = self.seqMod(pattern)
        patternLength = len(pattern) # length of window
        sideLength = patternLength/2
        errTol = 0.5 #todo 1 means high correlation
        thresLow = 70
        thresHigh = 300
        dataLen = len(data)
        peakIdx = []
        peakLabel = []
        outputIdx = []
        dataSeq = []
        dataMod = []
        normCorr = []

        if math.fmod(patternLength,2) == 0: # odd
            cenPtr =  patternLength/2
        else:
            cenPtr = (patternLength - 1)/2 # even


        corrSeq = np.correlate(data,pattern)

        for i in range((patternLength - 1), dataLen): # move the window from begin of the data to the end

            index = i - (patternLength - 1) # the step of move of the window
            dataSeq = data[index : (i+1)]
            dataMod.append(self.seqMod(dataSeq))

        for ii in range(0,len(corrSeq)):
            normCorr.append(corrSeq[ii]/dataMod[ii]/patternPower)


        outputIdx_corr = np.where(np.asarray(normCorr) > errTol)
        (blinkIndex,) = outputIdx_corr
        blinkIndex = blinkIndex.tolist()
        idxLen = len(blinkIndex)
        # print ('Indexs',idxLen)
        # print blinkIndex


        if idxLen != 0:
            idxLast = blinkIndex[idxLen-1]
            idxFirst = blinkIndex[0]
            if idxLast < 360:
                print 'last'
                for i in range(0,rpLen):
                    replace_pattern[i] = data[idxLast + int((480-idxLast)/2) - rpLen/2 + i]
            else:
                if idxFirst > 180:
                    print 'first'
                    for i in range(0,rpLen):
                        replace_pattern[i] = data[int(idxFirst/2) - rpLen/2 + i]
                else:
                    for i in range(0,idxLen-1):
                        if blinkIndex[i+1] - blinkIndex[i] > 200:
                            print 'middle'
                            for ii in range(0,rpLen):
                                z = math.ceil((blinkIndex[i+1] - blinkIndex[i])/2)
                                a = blinkIndex[i] + z - rpLen/2 + ii
                                replace_pattern[ii] = data[int(a)]
        # print replace_pattern
        # print outputIdx_corr
        outputSeq = np.asarray(data)

        for i in outputIdx_corr:
            for ii in range(0,patternLength):
                outputSeq[i+ii] = replace_pattern[ii%rpLen]


        # Output the center point index of the detected pattern
        outputIdx_corr2 = [x + cenPtr for x in outputIdx_corr]
        seq1 = np.asarray(data)[outputIdx_corr2]
        # (Idx1,) = np.where(seq1 > thresLow )
        # (Idx2,) = np.where(seq1 < thresHigh)
        # outputIdx = np.intersect1d(Idx1,Idx2)
        # print(outputIdx_corr2)
        return outputSeq


    def seqMod(self, data):
    #  Calculate the mod of a sequence

        dataMod = math.sqrt(sum(i * i for i in data))
        return dataMod


    # def attentionLevelToSpeed():
    #     tmp = self.scalEngInd
    #     self.motor_speed

