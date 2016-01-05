# -*- coding: utf-8 -*-

__all__ = ["contextmatrix", "doubly_lexical_order", "clusters", "graph", "lattice", "hierarchical_decomposition",
           "graphics", "mst", "triangle", "progress_status", "progress_bar", "cluster_order"]


from .progress_bar import ProgressBarPlaceholder


progress_status = ProgressBarPlaceholder()


def reset_progress_status():
    global progress_status
    progress_status = ProgressBarPlaceholder()