use nannou::image;
use nannou::image::GenericImageView;
use nannou::prelude::*;
use nannou::rand::{thread_rng, Rng};

struct Model {
    image: image::DynamicImage,
    dvd_rect: Rect,
    dvd_vel: Vec2,
    m_pos: Option<Vec2>,
}

fn main() {
    nannou::app(model).update(update).run();
}

fn model(app: &App) -> Model {
    let primary_window_id = app
        .new_window()
        .event(window_event)
        .view(view)
        .fullscreen()
        .build()
        .unwrap();

    let primary_window = app.window(primary_window_id).unwrap();
    primary_window.set_cursor_visible(false);

    let img_data = include_bytes!("../assets/dvd_logo.png");
    let image = image::load_from_memory(img_data)
        .unwrap()
        .thumbnail(
            app.window_rect().w() as u32 / 2,
            app.window_rect().h() as u32 / 2,
        )
        .huerotate(thread_rng().gen_range(120..240));
    let rect = Rect::from_x_y_w_h(
        0.0,
        0.0,
        image.dimensions().0 as f32,
        image.dimensions().1 as f32,
    );

    Model {
        image,
        dvd_rect: rect,
        // Velocity is in pixels per second.
        dvd_vel: Vec2::new(50.0, 50.0),
        m_pos: None,
    }
}

fn window_event(app: &App, model: &mut Model, event: WindowEvent) {
    match event {
        WindowEvent::MouseMoved(pos) => {
            if model.m_pos.is_none() {
                model.m_pos = Some(pos)
            }
            if app.time > 0.1 && model.m_pos.unwrap() != pos {
                app.quit()
            }
        }
        WindowEvent::MousePressed(..) => app.quit(),
        WindowEvent::KeyPressed(..) => app.quit(),
        WindowEvent::MouseWheel(..) => app.quit(),
        _ => (),
    }
}

fn update(app: &App, model: &mut Model, _update: Update) {
    let win = app.window_rect();
    let dvd_vel = &mut model.dvd_vel;
    model.dvd_rect = model
        .dvd_rect
        .shift_x(dvd_vel.x * app.duration.since_prev_update.secs() as f32)
        .shift_y(dvd_vel.y * app.duration.since_prev_update.secs() as f32);
    let rect = model.dvd_rect;

    if rect.left() <= win.left() || rect.right() >= win.right() {
        dvd_vel.x = -dvd_vel.x;
        model.image = model.image.huerotate(thread_rng().gen_range(120..240));
    }
    if rect.bottom() <= win.bottom() || rect.top() >= win.top() {
        dvd_vel.y = -dvd_vel.y;
        model.image = model.image.huerotate(thread_rng().gen_range(120..240));
    }
}

fn view(app: &App, model: &Model, frame: Frame) {
    let draw = app.draw();
    let texture = wgpu::Texture::from_image(app, &model.image);

    draw.texture(&texture)
        .xy(model.dvd_rect.xy())
        .wh(model.dvd_rect.wh());

    frame.clear(BLACK);
    draw.to_frame(app, &frame).unwrap();
}
