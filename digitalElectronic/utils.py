import typing as t
import bisect

import numpy as np
import manim
from manim import (
    VGroup,
    VMobject,
    Rectangle,
    Square,
    Circle,
    Triangle,
    Arc,
    Text,
    Tex,
    MathTex,
    Axes,
    DashedLine,
)
from manim import LEFT, RIGHT, UP, DOWN, UL, DL, UR, DR, ORIGIN
import manim.utils.color as C


# 绘制波形图
def get_wave_fig(
    func: t.Callable[[float], float],
    x_range: t.Sequence[float],
    x_range_axis: t.Sequence[float] = None,
    y_range_axis: t.Sequence[float] = [0, 1.3, 1],
    scale: float = 0.23,
    tex_scale: float = 1.5,
    stroke_width: float = 2,
    x_label: str = "t",
    draw_y_label=False,
    y_label: str = None,
    low_level: float = 0.1,
):
    ax = Axes(
        x_range=(
            x_range_axis if x_range_axis else [x_range[0], x_range[1] * 1.1, x_range[2]]
        ),
        y_range=y_range_axis,
        tips=True,
        axis_config={
            "include_numbers": False,
            "include_ticks": False,
            "tip_width": 0.2,
        },
    )
    graph = ax.plot(
        lambda x: func(x) + low_level,
        x_range=x_range,
        use_smoothing=False,
        stroke_width=stroke_width,
    )
    x_label_object = ax.get_x_axis_label(
        MathTex(x_label).scale(tex_scale), edge=DR, direction=DOWN
    )

    o_label_object = MathTex("O").scale(tex_scale).move_to(ax.get_origin() + DL * 0.4)
    if draw_y_label:
        y_label_object = ax.get_y_axis_label(
            MathTex(y_label).scale(tex_scale), edge=UL, direction=RIGHT, buff=0.4
        )
        group = [ax, graph, x_label_object, y_label_object, o_label_object]
    else:
        group = [ax, graph, x_label_object, o_label_object]
    return VGroup(*group).scale(scale), group


def draw_dashlines(
    start: manim.Axes,
    end: manim.Axes,
    xs: t.Sequence[float],
    stroke_width: float = 2,
    low_level: float = 0.1,
):
    dsls = []
    for x in xs:
        dsls.append(
            DashedLine(
                start.c2p([[x, 1 + low_level, 0]]),
                end.c2p([[x, 0, 0]]),
                stroke_width=stroke_width,
            )
        )
    return VGroup(*dsls)


def tab2func(x:t.Sequence[float],y:t.Sequence[float]) -> t.Callable[[float],float]:
    p = sorted(zip(x, y))
    xs, ys = zip(*p)
    
    def interp(t_: float) -> float:
        i = bisect.bisect_left(xs, t_)
        if i == 0:
            return ys[0]
        if i >= len(xs):
            return ys[-1]
        x0, x1 = xs[i - 1], xs[i]
        y0, y1 = ys[i - 1], ys[i]
        return y0 + (y1 - y0) * (t_ - x0) / (x1 - x0)

    return interp