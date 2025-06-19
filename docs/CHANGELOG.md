# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.1.9] - 2025-06-19
### :boom: BREAKING CHANGES
- due to [`b2d06da`](https://github.com/deargen/workflows/commit/b2d06da0745eb9b86256d10540b358ab91e1f623) - remove parse-changelog *(commit by [@kiyoon](https://github.com/kiyoon))*:

  remove parse-changelog


### :sparkles: New Features
- [`bd60f2e`](https://github.com/deargen/workflows/commit/bd60f2eac2c9129f4ea33c03b48eef30c3b04faf) - hatchling for get_src_dir *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`83f34fe`](https://github.com/deargen/workflows/commit/83f34fe2e3c02eb3aa6c9f98cc80c6a4874fe683) - add TC010 rule to essential *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`cf41e35`](https://github.com/deargen/workflows/commit/cf41e353761d82fafbaefd919fdd6fcdfcfebd8f) - **apply-ruff**: ruff extend ignore *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`a7b82e0`](https://github.com/deargen/workflows/commit/a7b82e06d4b4765ceeb2128370e72c5686877319) - parse-changelog *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`b2d06da`](https://github.com/deargen/workflows/commit/b2d06da0745eb9b86256d10540b358ab91e1f623) - remove parse-changelog *(commit by [@kiyoon](https://github.com/kiyoon))*

### :bug: Bug Fixes
- [`b974025`](https://github.com/deargen/workflows/commit/b974025f3545e6bfd6a0ea3877de65c370a635be) - deploy *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`63d747b`](https://github.com/deargen/workflows/commit/63d747b69066147ff5a133375250323c5eb03740) - cwd in check-ruff-only-changed *(commit by [@kiyoon](https://github.com/kiyoon))*

### :wrench: Chores
- [`81051f9`](https://github.com/deargen/workflows/commit/81051f97b334017f5b1260af997e69478d6faa7a) - remove comments *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`75923f9`](https://github.com/deargen/workflows/commit/75923f920afbf9571ababe02d50aeaaa915d3090) - remove unused option *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`7c886bd`](https://github.com/deargen/workflows/commit/7c886bd664484c83c9220f566c2961df86814f86) - deprecation *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.8] - 2024-12-24
### :boom: BREAKING CHANGES
- due to [`b7aa937`](https://github.com/deargen/workflows/commit/b7aa937643a4ed5101c8496f125385cb525c506a) - remove get-versioneer-version *(commit by [@kiyoon](https://github.com/kiyoon))*:

  remove get-versioneer-version


### :sparkles: New Features
- [`b7aa937`](https://github.com/deargen/workflows/commit/b7aa937643a4ed5101c8496f125385cb525c506a) - remove get-versioneer-version *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`e4340c0`](https://github.com/deargen/workflows/commit/e4340c03d80e22bb60762c364644b5e6bed57954) - automatically update version tag in deploy.yml *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`b716e73`](https://github.com/deargen/workflows/commit/b716e73d7ab39015c32bdb534532a78b9c6f42b3) - create pull request when deploy *(commit by [@kiyoon](https://github.com/kiyoon))*

### :bug: Bug Fixes
- [`45c2c28`](https://github.com/deargen/workflows/commit/45c2c2895756b4573bb23dff199e8d56cfbe42c0) - do not leave temporary tag when deployment fails *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`2e3ad1b`](https://github.com/deargen/workflows/commit/2e3ad1b5e74de1539fef376ddd8a98abac99a397) - python 3.8 doctest *(commit by [@kiyoon](https://github.com/kiyoon))*

### :wrench: Chores
- [`d299b19`](https://github.com/deargen/workflows/commit/d299b19b57839ed46b28a79454ad3e8f2a3a5d86) - fix ruff *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`30362c8`](https://github.com/deargen/workflows/commit/30362c8a4344ff99dc3019fa2a444c0a4eefa71b) - fix ruff *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.7] - 2024-12-17
### :sparkles: New Features
- [`4646ff1`](https://github.com/deargen/workflows/commit/4646ff1cbe9392ba5ba1bd10adc145242ed572bc) - raise KeyError if src/ not exists *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`96265d1`](https://github.com/deargen/workflows/commit/96265d195d86aef1dcec6625689591043240614c) - cwd for run-pytest and run-doctest *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`e99efa3`](https://github.com/deargen/workflows/commit/e99efa3e0c7d415d56af820d3875c749365e8dea) - gen-init-py with ruff. gen-init-py and check-mkdocs src-dir deprecated. *(commit by [@kiyoon](https://github.com/kiyoon))*

### :bug: Bug Fixes
- [`fde9694`](https://github.com/deargen/workflows/commit/fde96948b737c5306b8e81a6bf7775cbac9fa9e6) - gen-init-py *(commit by [@kiyoon](https://github.com/kiyoon))*

### :wrench: Chores
- [`5a3148f`](https://github.com/deargen/workflows/commit/5a3148f963610eb658ae239a07332f070b975ada) - fix doctest *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`5e7e514`](https://github.com/deargen/workflows/commit/5e7e5146c8315642bd6650d89704dd1debff7faf) - fix ruff *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.6] - 2024-12-13
### :sparkles: New Features
- [`aa4eedd`](https://github.com/deargen/workflows/commit/aa4eedd17a9f09fb1ce80f728ff62042c59df4b9) - **projector**: get-versioneer-version *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`7f0906e`](https://github.com/deargen/workflows/commit/7f0906ee45b9927b5b5c0ea06cda4243476d5a5c) - **projector**: expose some apis *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.5] - 2024-12-13
### :boom: BREAKING CHANGES
- due to [`40a4a2e`](https://github.com/deargen/workflows/commit/40a4a2ef9a3c652cda0081c2e349fdcf51456130) - change default gitlab branch to master *(commit by [@kiyoon](https://github.com/kiyoon))*:

  change default gitlab branch to master

- due to [`4732513`](https://github.com/deargen/workflows/commit/4732513f705ea81aefc7e8eacc0bdf4039fa4b03) - move configuration to pyproject.toml *(commit by [@kiyoon](https://github.com/kiyoon))*:

  move configuration to pyproject.toml


### :sparkles: New Features
- [`40a4a2e`](https://github.com/deargen/workflows/commit/40a4a2ef9a3c652cda0081c2e349fdcf51456130) - change default gitlab branch to master *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`f8889a4`](https://github.com/deargen/workflows/commit/f8889a4e00f37c0b233d6d4feb2eb42a27faca3b) - drop windows as default target platform *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`88fc58f`](https://github.com/deargen/workflows/commit/88fc58fcc159da35d8d1c393313800ef5d97e8b8) - **run-pytest**: additional-args *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`53a2d26`](https://github.com/deargen/workflows/commit/53a2d26e987a443e819c06aae9dfcbfee9a8e5bf) - ruff with additional args *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`40ab424`](https://github.com/deargen/workflows/commit/40ab4248130f1d4749a2d21f23bc1825c8019d7b) - exclude success in ruff lint summary *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`294bd94`](https://github.com/deargen/workflows/commit/294bd9437574094a7510d937e00555a4a45cf8b7) - **check-ruff**: lint-essential *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`5c568db`](https://github.com/deargen/workflows/commit/5c568db01e3fecd6f2695c2724a68fffcabffb83) - **ruff**: option to skip version file, and cwd. Partial monorepo support *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`6627cae`](https://github.com/deargen/workflows/commit/6627caeeee5a9ba0feb0220ab1ded24839cbd15a) - python-projector *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`4732513`](https://github.com/deargen/workflows/commit/4732513f705ea81aefc7e8eacc0bdf4039fa4b03) - **pip-compile**: move configuration to pyproject.toml *(commit by [@kiyoon](https://github.com/kiyoon))*

### :bug: Bug Fixes
- [`256b192`](https://github.com/deargen/workflows/commit/256b19286d3f34b23de1ed13c966132a01ef5032) - silence unwanted error msg when .venv not being used *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`188a896`](https://github.com/deargen/workflows/commit/188a896dd4ca417fe784d48f5407d59e2f14d956) - pip break-system-packages *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`1e41365`](https://github.com/deargen/workflows/commit/1e41365a21be76b03ff5ce374c349052fa789797) - pip --break-system-packages *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`5eca705`](https://github.com/deargen/workflows/commit/5eca705e8c1e72e61ce721e40ddb287fc977404a) - ci break-system-packages *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`bbc51d9`](https://github.com/deargen/workflows/commit/bbc51d9a6cc6af56697bf811edac106df0f197b1) - pip version issue by upgrading ubuntu *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`c75212c`](https://github.com/deargen/workflows/commit/c75212ca66baaef5dec211555fd5a5a1c7947847) - **docs**: dry-run was not working *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`868b864`](https://github.com/deargen/workflows/commit/868b86496ddb8636a3c943197bd2dbc40a4d73e4) - macos target to 13 (x86_64) or 14 (aarch64) *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`5bde1ca`](https://github.com/deargen/workflows/commit/5bde1ca26991b32d053fa47fe9b7c493acddb95e) - check mkdocs *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`6ad9ef0`](https://github.com/deargen/workflows/commit/6ad9ef09b26a7699c61509ced5246f5d00594f18) - no need higher macosx target as reduce-binary is built for lower *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`f0299d8`](https://github.com/deargen/workflows/commit/f0299d8bdbfb18d9f98807eb66c390e31b49e0b5) - **deploy-mkdocs**: clashing branch name when using master for pages *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`16d767b`](https://github.com/deargen/workflows/commit/16d767b4917645501d785ffb037bee1799695fe6) - check-ruff without additional_args *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`7899f8c`](https://github.com/deargen/workflows/commit/7899f8c50ab1fb12adfc6bed616cc858b60cef5b) - really fix additional args *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`4474845`](https://github.com/deargen/workflows/commit/4474845625739e5a227532c32cf30c01daddd2ed) - really fix additional-args *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`03f5153`](https://github.com/deargen/workflows/commit/03f515366216c8ed15092fb6bd900fbfb742d9d2) - really *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`14fbbc6`](https://github.com/deargen/workflows/commit/14fbbc6360cdf9f472c034a81b7b9953554d1e4c) - **check-ruff**: code annotation with additional_args *(commit by [@kiyoon](https://github.com/kiyoon))*

### :zap: Performance Improvements
- [`ca319e1`](https://github.com/deargen/workflows/commit/ca319e116690136aab7abdde6c410d9d22067f0f) - faster test output with tee *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.4] - 2024-09-26
### :sparkles: New Features
- [`2a3d1d9`](https://github.com/deargen/workflows/commit/2a3d1d99425aceafc4019dad7fc7b01d13645f39) - setup-micromamba-and-uv *(commit by [@kiyoon](https://github.com/kiyoon))*

### :bug: Bug Fixes
- [`08ca22e`](https://github.com/deargen/workflows/commit/08ca22ed9899d8bed8c149bd6a146641a64aef56) - **pip-compile**: use x86_64-manylinux_2_28 *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.3] - 2024-08-22
### :sparkles: New Features
- [`6c43fd8`](https://github.com/deargen/workflows/commit/6c43fd864bb628617d511e55d596eecaf9105d24) - mkdocs github pages *(commit by [@kiyoon](https://github.com/kiyoon))*

### :bug: Bug Fixes
- [`e5ff0fc`](https://github.com/deargen/workflows/commit/e5ff0fc2d00d2dd09fa5451ca0e403311ec1d25d) - doctest failing in some cases for __init__ modules *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`5e0a8cb`](https://github.com/deargen/workflows/commit/5e0a8cb006ceb5ecf74d23f234640a5ae75d9a09) - mkdocs github pages *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`4038c46`](https://github.com/deargen/workflows/commit/4038c468cf1d84030abfc475962d4e63556c008b) - github pages mkdocs *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`d6f321a`](https://github.com/deargen/workflows/commit/d6f321ad3d6a1a4aed5d1c8462b71e73ca9e239e) - mkdocs github pages needs to fetch the branch first *(commit by [@kiyoon](https://github.com/kiyoon))*

### :wrench: Chores
- [`95dffc7`](https://github.com/deargen/workflows/commit/95dffc7a3e946708320952993ae6ffc4edfbe3e9) - fix wrong job name *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.2] - 2024-07-12
### :bug: Bug Fixes
- [`897fe03`](https://github.com/deargen/workflows/commit/897fe03b5d3259c541761a47506446c2304f4c20) - apply ruff *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`fdde174`](https://github.com/deargen/workflows/commit/fdde174086c9ee7fe2aed22b58cb509a43ce27c8) - **pip-compile**: exit with error *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`b41721a`](https://github.com/deargen/workflows/commit/b41721a6e00c996eb4a72c793cb200713453b825) - mkdocs proper python version *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`234ce89`](https://github.com/deargen/workflows/commit/234ce896796df393d53964fa9e387453da32e5da) - deploy-mkdocs *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.1] - 2024-07-02
### :sparkles: New Features
- [`8dcbc64`](https://github.com/deargen/workflows/commit/8dcbc645c491b166a442a748372f81a13df603d6) - setup-conda *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`c305995`](https://github.com/deargen/workflows/commit/c305995e86d025780e54f22500212edf764901ae) - check mkdocs build *(commit by [@kiyoon](https://github.com/kiyoon))*


## [v0.1.0] - 2024-07-02
### :bug: Bug Fixes
- [`18e96ff`](https://github.com/deargen/workflows/commit/18e96fff440691348fd0783f1b77507019b56859) - wrong environment *(commit by [@kiyoon](https://github.com/kiyoon))*
- [`3e3d754`](https://github.com/deargen/workflows/commit/3e3d754d17efa8fbea27c889447ea614c8d1e7f4) - **doctest**: uv activate *(commit by [@kiyoon](https://github.com/kiyoon))*

[v0.1.0]: https://github.com/deargen/workflows/compare/v0.0.0...v0.1.0
[v0.1.1]: https://github.com/deargen/workflows/compare/v0.1.0...v0.1.1
[v0.1.2]: https://github.com/deargen/workflows/compare/v0.1.1...v0.1.2
[v0.1.3]: https://github.com/deargen/workflows/compare/v0.1.2...v0.1.3
[v0.1.4]: https://github.com/deargen/workflows/compare/v0.1.3...v0.1.4
[v0.1.5]: https://github.com/deargen/workflows/compare/v0.1.4...v0.1.5
[v0.1.6]: https://github.com/deargen/workflows/compare/v0.1.5...v0.1.6
[v0.1.7]: https://github.com/deargen/workflows/compare/v0.1.6...v0.1.7
[v0.1.8]: https://github.com/deargen/workflows/compare/v0.1.7...v0.1.8
[v0.1.8]: https://github.com/deargen/workflows/compare/v0.1.7...v0.1.8
[v0.1.9]: https://github.com/deargen/workflows/compare/v0.1.8...v0.1.9
