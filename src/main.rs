//! Renders a 2D scene containing a single, moving sprite.

use bevy::asset::embedded_asset;
use bevy::prelude::*;
use bevy::window::WindowMode;

struct EmbeddedAssetPlugin;

impl Plugin for EmbeddedAssetPlugin {
    fn build(&self, app: &mut App) {
        embedded_asset!(app, "assets/dvd_logo.png");
    }
}

#[derive(Component)]
enum Direction {
    Up,
    Down,
}

fn main() {
    App::new()
        .add_plugins((
            DefaultPlugins.set(WindowPlugin {
                primary_window: Some(Window {
                    resizable: false,
                    position: WindowPosition::Automatic,
                    mode: WindowMode::Fullscreen(MonitorSelection::Primary),
                    visible: true,
                    ..default()
                }),
                ..default()
            }),
            EmbeddedAssetPlugin,
        ))
        .add_systems(Startup, setup)
        .add_systems(Update, sprite_movement)
        .run();
}

fn setup(mut commands: Commands, asset_server: Res<AssetServer>) {
    commands.spawn(Camera2d);
    commands.spawn((
        Sprite::from_image(asset_server.load("embedded://dvd_screensaver/assets/dvd_logo.png")),
        Transform::from_xyz(100.0, 0.0, 0.0),
        Direction::Up,
    ));
}

fn sprite_movement(time: Res<Time>, mut sprite_position: Query<(&mut Direction, &mut Transform)>) {
    for (mut logo, mut transform) in &mut sprite_position {
        match *logo {
            Direction::Up => transform.translation.y += 150.0 * time.delta_secs(),
            Direction::Down => transform.translation.y -= 150.0 * time.delta_secs(),
        }

        if transform.translation.y > 200.0 {
            *logo = Direction::Down;
        } else if transform.translation.y < -200.0 {
            *logo = Direction::Up;
        }
    }
}
