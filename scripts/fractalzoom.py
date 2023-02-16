from modules import script_callbacks, sd_samplers, call_queue
import gradio as gr

def myprocess(*args, **kwargs):
    """
    _steps
    _sampler_index
    _width
    _height
    _cfg_scale
    _denoising_strength
    _total_time
    _fps
    _smoothing
    _film_interpolation
    _add_noise
    _noise_strength
    _seed
    _seed_travel
    _initial_img
    _loopback_mode
    _prompt_interpolation
    _tmpl_pos
    _tmpl_neg
    _key_frames
    _vid_gif
    _vid_mp4
    _vid_webm
    _style_pos
    _style_neg
    """

    # Build a dict of the settings, so we can easily pass to sub functions.
    myset = {'steps': args[i + 0],  # int(_steps),
             'sampler_index': args[i + 1],  # int(_sampler_index),
             'width': args[i + 2],  # int(_width),
             'height': args[i + 3],  # int(_height),
             'cfg_scale': args[i + 4],  # float(_cfg_scale),
             'denoising_strength': args[i + 5],  # float(_denoising_strength),
             'total_time': args[i + 6],  # float(_total_time),
             'fps': args[i + 7],  # float(_fps),
             'smoothing': args[i + 8],  # int(_smoothing),
             'film_interpolation': args[i + 9],  # int(_film_interpolation),
             'add_noise': args[i + 10],  # _add_noise,
             'noise_strength': args[i + 11],  # float(_noise_strength),
             'seed': args[i + 12],  # int(_seed),
             'seed_travel': args[i + 13],  # bool(_seed_travel),

             'loopback': args[i + 15],  # bool(_loopback_mode),
             'prompt_interpolation': args[i + 16],  # bool(_prompt_interpolation),
             'tmpl_pos': args[i + 17],  # str(_tmpl_pos).strip(),
             'tmpl_neg': args[i + 18],  # str(_tmpl_neg).strip(),
             'key_frames': args[i + 19],  # str(_key_frames).strip(),
             'vid_gif': args[i + 20],  # bool(_vid_gif),
             'vid_mp4': args[i + 21],  # bool(_vid_mp4),
             'vid_webm': args[i + 22],  # bool(_vid_webm),
             '_style_pos': args[i + 23],  # str(_style_pos).strip(),
             '_style_neg': args[i + 24],  # str(_style_neg).strip(),
             'source': "",
             'debug': os.path.exists('debug.txt')}

def ui_block_generation():
    with gr.Blocks():
        steps = gr.Slider(minimum=1, maximum=150, step=1, label="Sampling Steps", value=20)
        sampler_index = gr.Radio(label='Sampling method', choices=[x.name for x in sd_samplers.samplers_for_img2img],value=sd_samplers.samplers_for_img2img[0].name, type="index")

        with gr.Group():
            with gr.Row():
                width = gr.Slider(minimum=64, maximum=2048, step=64, label="Width", value=512)
                height = gr.Slider(minimum=64, maximum=2048, step=64, label="Height", value=512)
        with gr.Group():
            with gr.Row():
                cfg_scale = gr.Slider(minimum=1.0, maximum=30.0, step=0.5, label='CFG Scale', value=7.0)
                denoising_strength = gr.Slider(minimum=0.0, maximum=1.0, step=0.01, label='Denoising strength', value=0.40)
        with gr.Row():
            seed = gr.Number(label='Seed', value=-1)
            seed_travel = gr.Checkbox(label='Seed Travel', value=False)

        gr.Button(value="Start", variant='primary', elem_id="sd_fractal_zoom_procbutton").click(fn=call_queue.wrap_gradio_gpu_call(myprocess, extra_outputs=[gr.update()]),
                       #_js="start_animator",
                       inputs=[steps, sampler_index, width, height, cfg_scale, denoising_strength, seed, seed_travel],
                       outputs=[])

    return steps, sampler_index, width, height, cfg_scale, denoising_strength, seed, seed_travel

#
# Basic layout of page
#
def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as fractalzoom_tabs:
        with gr.Row():
            with gr.Column():
                with gr.Tab("Generation"):
                    steps, sampler_index, width, height, cfg_scale, denoising_strength, seed, seed_travel = ui_block_generation()

    return (fractalzoom_tabs, "Fractal Zoom", "sd-fractal-zoom"),


script_callbacks.on_ui_tabs(on_ui_tabs)