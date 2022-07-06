from controllers.TrackController import TrackController

def main():
    # TODO: Create command for choise
    track_controller = TrackController()
    # track_controller.add_new_tracks_to_playlist()
    # track_controller.remove_tracks_from_playlist()
    track_controller.show_current_track_from_csv()


if __name__ == "__main__":
    main()

