from pathlib import Path
import os

import geopandas as gpd
import matplotlib.pyplot as plt
from PIL import Image


# =========================
# 路径设置
# =========================

PROJECT_DIR = Path(r"D:\琼岛智划_project")

# 你的原始 DRL 项目路径
DRL_DIR = Path(r"D:\DRL-urban-planning-main\DRL-urban-planning-main")

OUTPUT_DIR = PROJECT_DIR / "outputs"
DATA_DIR = PROJECT_DIR / "data"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_one(name: str):
    """
    name: dhm 或 hlg
    """
    geojson_path = DRL_DIR / "results" / f"{name}.geojson"
    output_img = OUTPUT_DIR / f"{name}_result_clean.png"
    output_csv = DATA_DIR / f"{name}_summary.csv"

    print("=" * 60)
    print(f"正在处理：{name}")
    print("geojson 路径：", geojson_path)
    print("geojson 是否存在：", geojson_path.exists())

    if not geojson_path.exists():
        print(f"错误：找不到 {geojson_path}")
        return

    gdf = gpd.read_file(geojson_path)

    print("读取成功")
    print("数据量：", len(gdf))
    print("列名：", list(gdf.columns))

    # 生成统计表
    gdf["geom_type"] = gdf.geometry.geom_type
    gdf["area"] = gdf.geometry.area
    gdf["length"] = gdf.geometry.length

    summary = gdf.groupby(["type", "geom_type"]).agg(
        count=("id", "count"),
        total_area=("area", "sum"),
        total_length=("length", "sum")
    ).reset_index()

    summary.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print("统计表已保存：", output_csv)

    # 生成图片
    fig, ax = plt.subplots(figsize=(8, 12))

    gdf.plot(
        ax=ax,
        column="type",
        categorical=True,
        legend=True,
        linewidth=0.6,
        edgecolor="black"
    )

    title = f"{name.upper()} Community Planning Result"
    ax.set_title(title, fontsize=16)
    ax.set_axis_off()

    plt.savefig(output_img, dpi=300, bbox_inches="tight", format="png")
    plt.close(fig)

    print("图片已保存：", output_img)
    print("图片大小：", output_img.stat().st_size, "bytes")

    # 检查图片是否真的有效
    try:
        img = Image.open(output_img)
        img.verify()
        print("图片校验成功，可以正常打开。")
    except Exception as e:
        print("图片校验失败：", e)


if __name__ == "__main__":
    generate_one("dhm")
    generate_one("hlg")

    print("=" * 60)
    print("全部处理完成。请检查：")
    print(OUTPUT_DIR / "dhm_result_clean.png")
    print(OUTPUT_DIR / "hlg_result_clean.png")
    print(DATA_DIR / "dhm_summary.csv")
    print(DATA_DIR / "hlg_summary.csv")