import numpy as np
import mathx as mx

def subtract_tangent(x,y,x_0,axis=None):
    if axis==None:
        axis=mx.last_axis(x)
    y_0=mx.interp_at(x,y,x_0,[0,1])
    return y-y_0[0]-(x-x_0)*y_0[1]


def line_two_points(x1, y1, x2, y2, x):
    return mx.divide0(y1*(x2 - x) + y2*(x - x1), x2 - x1, float('nan'))


def peak_crossings_1D(x, y, frac=0.5, ym=None):
    """
    Args:
        x: increasing array
        y: function sampled at x
        ym: if supplied, use as maximum instead
    """
    x = np.asarray(x)
    y = np.asarray(y)
    im = y.argmax()
    if ym is None:
        ym = y[im]
    yc = ym*frac
    # after
    ais = im + (y[im:] < yc).nonzero()[0]
    if len(ais) == 0:
        ai = len(x) - 1  # x[-1]
    else:
        ai = ais[0]  # a=x[ai]-x[ai-1]
    a = line_two_points(y[ai - 1], x[ai - 1], y[ai], x[ai], yc)
    # before
    bis = im - (y[im::-1] < ym*frac).nonzero()[0]
    if len(bis) == 0:
        bi = 0
    else:
        bi = min(bis[0], len(x) - 2)
    b = line_two_points(y[bi], x[bi], y[bi + 1], x[bi + 1], yc)
    return b, a


def peak_crossings(x, y, frac=0.5, axis=None, ym=None):
    if axis is None:
        axis = mx.last_axis(x)
    if ym is None:
        return mx.eval_iterated(lambda x, y: peak_crossings_1D(x, y, frac), (x, y), vec_dims=[axis])
    else:
        return mx.eval_iterated(lambda x, y, ym: peak_crossings_1D(x, y, frac, ym), (x, y, ym), vec_dims=[axis])


def fwhm(x, y, axis=None):
    x1, x2 = peak_crossings(x, y, 0.5, axis)
    return x2 - x1


def find_peaks_iter_rmv(y, n, Dy_thresh=0, max_half_int=float('inf'), cyclic=False, min_half_int=-float('inf')):
    """Finds peaks using 'iterative removal'.

    The maximum value is recorded as a peak. Then, an interval
    around this maximum is removed. The interval is defined by the closest local
    minima or max_half_int, whichever is smaller. Local minima are defined by
    y rising from the minimum by Dy_thresh.
    Args:
        y (sequence): vector in which to find peaks
        n (int): number of peaks
        Dy_thresh (float): Minimum increase to declare a local minimum
        max_half_int (float): maximum distance from peak for removal
        cyclic (bool): cyclic boundary conditions
    Returns: the peaks in order of discovery.
        """
    y = y.copy()  # we change it
    min_y = y.min()  # set 'removed' intervals to this

    def find_rmv_peak():
        ind_peak = y.argmax()

        def scan(ind, dir):
            if cyclic:
                stop_ind = None
            else:
                if dir > 0:
                    stop_ind = len(y) - 1
                else:
                    stop_ind = 0
            scan_min_y = y[ind]
            scan_min_ind = ind
            dist = 0
            halt = False
            while ind != stop_ind:
                # Have we risen out of a minimum?
                if y[ind + dir] - scan_min_y > Dy_thresh:
                    halt = True
                if dist >= min_half_int and halt:
                    break
                if dist == max_half_int:
                    break
                ind += dir
                dist += 1
                # Update minimum
                if y[ind] < scan_min_y:
                    scan_min_y = y[ind]
                    scan_min_ind = ind
            return scan_min_ind

        # Set interval to minimum
        left_ind = scan(ind_peak, -1)
        right_ind = scan(ind_peak, 1)
        y[left_ind:right_ind + 1] = min_y
        return ind_peak

    ind_peaks = []
    for _ in range(n):
        ind_peaks.append(find_rmv_peak())
    return ind_peaks