import numpy as np

from class_measures_result import dbm_to_mw, mw_to_dbm, linear_mean

def is_standard_pattern(result):
    """
    Return True only for regular codebook/results patterns.
    Excludes reference / min / max patterns with idx >= 100000.
    """
    return result.idx < 100000


def get_ids_for_mode(ref_in_range, mode):
    """
    Extract reference IDs for selected mode.

    ref_in_range can be:
    - None
    - list / range / tuple
    - dict with keys: 'max', 'min'
    """

    if ref_in_range is None:
        return None

    if isinstance(ref_in_range, dict):
        return ref_in_range.get(mode, None)

    return ref_in_range


def select_ref_results(results_obj, ids, mode):
    """
    Select reference candidates from results.maxs or results.mins by idx.

    mode:
        'max' -> use results.maxs
        'min' -> use results.mins
    """

    if mode == 'max':
        ref_source = results_obj.maxs
    elif mode == 'min':
        ref_source = results_obj.mins
    else:
        raise ValueError("mode must be 'max' or 'min'")

    if ids is None:
        return ref_source

    ids_set = set(ids)

    selected = []
    for result in ref_source:
        if result.idx in ids_set:
            selected.append(result)

    return selected


def get_trace_for_position(result, target_rx, target_c, rx_tol=1e-6, c_tol=1e-6):
    """
    Return truncated trace for given measurement position:
        (Rx_Angle, c_value)

    Returns None if position is not found.
    """

    for i in range(len(result.traces)):
        rx_ok = abs(result.Rx_Angle[i] - target_rx) <= rx_tol
        c_ok = abs(result.c_values[i] - target_c) <= c_tol

        if rx_ok and c_ok:
            return result.traces[i].get_truncaded_trace()

    return None


def result_avg_for_position(result, target_rx, target_c, rx_tol=1e-6, c_tol=1e-6):
    """
    Linear average of one Result trace at selected (Rx, c) position.
    """

    trace_dbm = get_trace_for_position(
        result=result,
        target_rx=target_rx,
        target_c=target_c,
        rx_tol=rx_tol,
        c_tol=c_tol
    )

    if trace_dbm is None:
        return np.nan

    return linear_mean(trace_dbm)


def result_avg_global(result):
    """
    Linear average of one Result over all available traces.
    Used when selection_scope='global'.
    """

    vals = []

    for trace in result.traces:
        trace_dbm = trace.get_truncaded_trace()
        vals.append(linear_mean(trace_dbm))

    if len(vals) == 0:
        return np.nan

    return linear_mean(np.array(vals))


def linear_avg_trace_for_position(result_list, target_rx, target_c, rx_tol=1e-6, c_tol=1e-6):
    """
    Linear average trace from given list of Result objects
    for selected (Rx, c) position.

    IMPORTANT:
    Patterns with idx >= 100000 are ignored.

    Returns:
        avg_trace_dbm : np.array or None
        avg_scalar_dbm : float
    """

    traces_mw = []

    for result in result_list:

        # Ignore reference / min / max patterns
        if not is_standard_pattern(result):
            continue

        trace_dbm = get_trace_for_position(
            result=result,
            target_rx=target_rx,
            target_c=target_c,
            rx_tol=rx_tol,
            c_tol=c_tol
        )

        if trace_dbm is None:
            continue

        traces_mw.append(dbm_to_mw(trace_dbm))

    if len(traces_mw) == 0:
        return None, np.nan

    traces_mw = np.array(traces_mw)

    # Mean over patterns, separately for each subcarrier.
    avg_trace_mw = np.mean(traces_mw, axis=0)
    avg_trace_dbm = mw_to_dbm(avg_trace_mw)

    # One scalar average from the average trace.
    avg_scalar_dbm = linear_mean(avg_trace_dbm)

    return avg_trace_dbm, avg_scalar_dbm

def codebook_linear_avg_for_position(cb_results, target_rx, target_c, rx_tol=1e-6, c_tol=1e-6):
    """
    Linear scalar average from all truncated traces of all regular patterns
    in one codebook for selected (Rx, c) position.

    IMPORTANT:
    Patterns with idx >= 100000 are ignored.

    Returns scalar in dBm.
    """

    traces_mw = []

    for result in cb_results.results:

        # Ignore reference / min / max patterns
        if not is_standard_pattern(result):
            continue

        trace_dbm = get_trace_for_position(
            result=result,
            target_rx=target_rx,
            target_c=target_c,
            rx_tol=rx_tol,
            c_tol=c_tol
        )

        if trace_dbm is None:
            continue

        traces_mw.append(dbm_to_mw(trace_dbm))

    if len(traces_mw) == 0:
        return np.nan

    traces_mw = np.array(traces_mw)

    avg_mw = np.mean(traces_mw)

    return mw_to_dbm(avg_mw)


def choose_codebook_result(cb_results,
                           target_rx,
                           target_c,
                           mode,
                           selection_scope='rx',
                           rx_tol=1e-6,
                           c_tol=1e-6):
    """
    Choose best/worst Result from one codebook.

    mode:
        'max' -> best pattern
        'min' -> worst pattern

    selection_scope:
        'rx':
            selection based on current (Rx, c) position.

        'global':
            selection based on all traces of a pattern.
            Displayed average still describes current plotted trace.
    """

    if len(cb_results.results) == 0:
        return None, np.nan

    scores = []

    for result in cb_results.results:
        if selection_scope == 'rx':
            score = result_avg_for_position(
                result=result,
                target_rx=target_rx,
                target_c=target_c,
                rx_tol=rx_tol,
                c_tol=c_tol
            )
        elif selection_scope == 'global':
            score = result_avg_global(result)
        else:
            raise ValueError("selection_scope must be one of: 'rx', 'global'")

        scores.append(score)

    scores = np.array(scores, dtype=float)
    valid_mask = ~np.isnan(scores)

    if not np.any(valid_mask):
        return None, np.nan

    valid_indices = np.where(valid_mask)[0]
    valid_scores = scores[valid_mask]

    if mode == 'max':
        selected_local_idx = int(np.argmax(valid_scores))
    elif mode == 'min':
        selected_local_idx = int(np.argmin(valid_scores))
    else:
        raise ValueError("mode must be 'max' or 'min'")

    selected_idx = valid_indices[selected_local_idx]
    selected_result = cb_results.results[selected_idx]

    plotted_avg = result_avg_for_position(
        result=selected_result,
        target_rx=target_rx,
        target_c=target_c,
        rx_tol=rx_tol,
        c_tol=c_tol
    )

    return selected_result, plotted_avg


def choose_ref_result_for_position(ref_results,
                                   target_rx,
                                   target_c,
                                   mode,
                                   rx_tol=1e-6,
                                   c_tol=1e-6):
    """
    Choose one reference trace for selected (Rx, c) position.

    mode:
        'max' -> reference with highest linear mean
        'min' -> reference with lowest linear mean
    """

    if len(ref_results) == 0:
        return None, np.nan

    scores = []

    for result in ref_results:
        score = result_avg_for_position(
            result=result,
            target_rx=target_rx,
            target_c=target_c,
            rx_tol=rx_tol,
            c_tol=c_tol
        )
        scores.append(score)

    scores = np.array(scores, dtype=float)
    valid_mask = ~np.isnan(scores)

    if not np.any(valid_mask):
        return None, np.nan

    valid_indices = np.where(valid_mask)[0]
    valid_scores = scores[valid_mask]

    if mode == 'max':
        selected_local_idx = int(np.argmax(valid_scores))
    elif mode == 'min':
        selected_local_idx = int(np.argmin(valid_scores))
    else:
        raise ValueError("mode must be 'max' or 'min'")

    selected_idx = valid_indices[selected_local_idx]

    return ref_results[selected_idx], scores[selected_idx]

def parse_optimization_result_id(idx):
    """
    Parse optimization result ID.

    ID format:
        first digit:
            1 -> maximization
            2 -> minimization

        middle digits:
            first optimized subcarrier N

        last two digits:
            i-th optimization in given localization/process

    Examples:
        1001000 -> mode=1, N=10, iteration=0
        1001017 -> mode=1, N=10, iteration=17
        2001000 -> mode=2, N=10, iteration=0
    """

    s = str(int(idx))

    if len(s) < 4:
        raise ValueError(f"Optimization ID {idx} is too short to parse.")

    mode_digit = int(s[0])
    iteration = int(s[-2:])
    n_str = s[1:-2]

    if n_str == "":
        raise ValueError(f"Optimization ID {idx} has empty N field.")

    opt_n = int(n_str)

    if mode_digit == 1:
        process = "max"
    elif mode_digit == 2:
        process = "min"
    else:
        raise ValueError(
            f"Optimization ID {idx} has invalid first digit: {mode_digit}. "
            "Expected 1 for max or 2 for min."
        )

    return {
        "process": process,
        "N": opt_n,
        "iteration": iteration,
        "idx": int(idx)
    }

def select_optimization_results(results, process, opt_N=None, iteration_range=None):
    """
    Select optimization results from results.maxs or results.mins.

    Parameters
    ----------
    results : Results
        Main Results object.

    process : str
        'max' -> use results.maxs
        'min' -> use results.mins

    opt_N : int or None
        First optimized subcarrier N.
        If None, accept all N.

    iteration_range : iterable or None
        Allowed optimization iterations.
        If None, accept all iterations.

    Returns
    -------
    selected : list of tuples
        List of:
            (result, parsed_id_dict)

        sorted by iteration.
    """

    if process not in ["max", "min"]:
        raise ValueError("process must be one of: 'max', 'min'")

    if process == "max":
        source = results.maxs
    else:
        source = results.mins

    if iteration_range is not None:
        iteration_set = set(iteration_range)
    else:
        iteration_set = None

    selected = []

    for result in source:
        try:
            parsed = parse_optimization_result_id(result.idx)
        except ValueError:
            continue

        if parsed["process"] != process:
            continue

        if opt_N is not None and parsed["N"] != opt_N:
            continue

        if iteration_set is not None and parsed["iteration"] not in iteration_set:
            continue

        selected.append((result, parsed))

    selected = sorted(selected, key=lambda x: x[1]["iteration"])

    return selected