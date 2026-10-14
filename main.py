from pipeline.bootstrap import build_use_case


def main() -> None:
    use_case = build_use_case()
    use_case.execute()


if __name__ == "__main__":
    main()
