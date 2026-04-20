from asciifier.renderers.base import RenderOpts


def test_render_opts_defaults():
    opts = RenderOpts(color_mode="truecolor")
    assert opts.color_mode == "truecolor"
    assert opts.invert is False
    assert opts.ramp == " .:-=+*#%@"
