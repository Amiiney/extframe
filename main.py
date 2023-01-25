import hydra
from extract_segment import segment

@hydra.main(config_name="config")
def run(CFG):
    segment(CFG)


if __name__ == "__main__":
    run()