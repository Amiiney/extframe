import hydra
from extract import extract_frames


@hydra.main(config_name="config")
def run(CFG):
    extract_frames(CFG)


if __name__ == "__main__":
    run()
