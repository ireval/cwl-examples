import sys
sys.path.insert(0, '../../cwl/scripts/')
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


from ruler.measures.cwl_ap import *
from ruler.measures.cwl_bpm import *
from ruler.measures.cwl_dcg import *
from ruler.measures.cwl_ift import *
from ruler.measures.cwl_inst import *
from ruler.measures.cwl_insq import *
from ruler.measures.cwl_precision import *
from ruler.measures.cwl_rbp import *
from ruler.measures.cwl_rr import *
from ruler.measures.cwl_tbg import *
from ruler.measures.cwl_umeasure import *
from ruler.cwl_ruler import Ranking


font = {
        'weight' : 'bold',
        'size'   : 24}

matplotlib.rc('font', **font)
matplotlib.rc('axes', linewidth=2)


ec1 = (0, 0, 0)
fc1 = (1, 1, 1)
ypos = 0.05
bbox1 = dict(boxstyle="round",ec=ec1, fc=fc1,)


def plot_text(text,xpos, ypos,bbox):
    plt.text(xpos, ypos, text, size=24, rotation=0.,
         ha="center", va="center",
         bbox=bbox
         )


def add_plot_labels(plt, ylabel, xlabel, title):

    plt.xticks(range(1,11))
    plt.xlabel(xlabel, fontweight="bold")
    plt.ylabel(ylabel, fontweight="bold")
    plt.title(title,fontweight="bold")
    plt.ylim([-0.03,1.03])


def plot_cwl_figures(metric, topics):

    topic_names = []
    for topic in topics:
        topic_names.append(topic.topic_id)

    n = 10
    x = range(1,n+1)
    fig = plt.figure()
    plt.figure(figsize=(15,5))
    plt.subplots_adjust(hspace=0.2)
    ax1 = plt.subplot(131)
    add_plot_labels(plt,"$C_i$",'Position ($i$)', "C Function")
    plt.legend(labels=topic_names)

    ax2 = plt.subplot(132)
    add_plot_labels(plt,"$W_i$",'Position ($i$)', "W Function")
    plt.legend(labels=topic_names)

    ax3 = plt.subplot(133)
    add_plot_labels(plt,"$L_i$",'Position ($i$)', "L Function")
    plt.legend(labels=topic_names)


    for topic in topics:
        metric.measure(topic)
        cvec = metric.c_vector(topic)
        wvec = metric.w_vector(topic)
        lvec = metric.l_vector(topic)

        plt.sca(ax1)
        plt.plot(x[0:10], cvec[0:n], 'x--', linewidth=3.0, markersize=8.0)

        plt.sca(ax2)
        plt.plot(x[0:10], wvec[0:n], 'x--', linewidth=3.0, markersize=8.0)
        plt.sca(ax3)
        plt.plot(x[0:10], lvec[0:n], 'x--', linewidth=3.0, markersize=8.0)


    plt.savefig("CWL-Plot-{}.eps".format(metric.metric_name.strip()),bbox_inches='tight',format='eps')
    plt.show()
    plt.close()



def make_metric_plots(EDs, EUs, ETUs, ETCs, topics, metric_name):
    fig = plt.figure()
    plt.figure(figsize=(5,15))
    ax1 = plt.subplot(311)
    add_plot_labels(plt, "Expected Utility (EU)", "Expected Depth (ED)", "{} over Theta".format(metric_name))


    ax2 = plt.subplot(312)
    add_plot_labels(plt, "Expected Total Utility (ETU)", "Expected Depth (ED)", "")
    plt.ylim([-0.03,3.03])

    ax3 = plt.subplot(313)
    add_plot_labels(plt, "Expected Total Cost (ETC)", "Expected Depth (ED)", "")
    plt.ylim([-0.03,20.03])

    topic_names = []
    for topic in topics:
        topic_names.append(topic.topic_id)
        plt.sca(ax1)
        plt.plot(EDs[topic.topic_id], EUs[topic.topic_id], 'o--', linewidth=3.0, markersize=8.0)

        plt.sca(ax2)
        plt.plot(EDs[topic.topic_id], ETUs[topic.topic_id], 'o--', linewidth=3.0, markersize=8.0)

        plt.sca(ax3)
        plt.plot(EDs[topic.topic_id], ETCs[topic.topic_id], 'o--', linewidth=3.0, markersize=8.0)


    plt.legend(labels=topic_names)

    plt.savefig("Measurement-Plot-{}.eps".format(metric_name.strip()),bbox_inches='tight',format='eps')
    plt.show()
    plt.close()

def make_rbp_plots(topics, thetas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]):


    rbp = RBPCWLMetric(theta=0.1)

    EUs = {}
    ETUs = {}
    ETCs = {}
    EDs = {}
    topic_names = []
    for topic in topics:
        EUs[topic.topic_id] = []
        EDs[topic.topic_id] = []
        ETUs[topic.topic_id] = []
        ETCs[topic.topic_id] = []
        topic_names.append(topic.topic_id)
        for theta in thetas:
            rbp.theta = theta
            rbp.measure(topic)
            EUs[topic.topic_id].append(rbp.expected_utility)
            ETUs[topic.topic_id].append(rbp.expected_total_utility)
            ETCs[topic.topic_id].append(rbp.expected_total_cost)
            EDs[topic.topic_id].append(rbp.expected_items)

    make_metric_plots(EDs,EUs,ETUs, ETCs, topics, "Rank Biased Precision (RBP)")




def make_tbg_plots(topics, halflives = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]):

    #halflives = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
    tbg = TBGCWLMetric(halflife=0.25)

    EUs = {}
    EDs = {}

    ETCs = {}
    ETUs = {}

    for topic in topics:
        EUs[topic.topic_id] = []
        EDs[topic.topic_id] = []
        ETUs[topic.topic_id] = []
        ETCs[topic.topic_id] = []

        for halflife in halflives:
            tbg.halflife = halflife
            tbg.measure(topic)
            EUs[topic.topic_id].append(tbg.expected_utility)
            EDs[topic.topic_id].append(tbg.expected_items)
            ETUs[topic.topic_id].append(tbg.expected_total_utility)
            ETCs[topic.topic_id].append(tbg.expected_total_cost)

    make_metric_plots(EDs,EUs,ETUs, ETCs, topics, "Time Biased Gain (TBG)")


def make_bpm_plots(topics, Ts = [ 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]):

    #Ts = [ 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    bpm = BPMDCWLMetric(T=2, K=10.0, hc=0.5, hb=0.5)

    EUs = {}
    EDs = {}
    ETCs = {}
    ETUs = {}

    for topic in topics:
        EUs[topic.topic_id] = []
        EDs[topic.topic_id] = []
        ETUs[topic.topic_id] = []
        ETCs[topic.topic_id] = []

        for T in Ts:
            bpm.T = T
            bpm.measure(topic)
            EUs[topic.topic_id].append(bpm.expected_utility)
            EDs[topic.topic_id].append(bpm.expected_items)
            ETUs[topic.topic_id].append(bpm.expected_total_utility)
            ETCs[topic.topic_id].append(bpm.expected_total_cost)

    make_metric_plots(EDs,EUs,ETUs, ETCs, topics, "Bejewelled Player Model (BPM)")
