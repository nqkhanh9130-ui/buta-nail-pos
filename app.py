import streamlit as st
import sqlite3, json, pandas as pd, plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(
    page_title="BUTA NAIL POS",
    page_icon="💅",
    layout="centered",          # ← KHÔNG dùng "wide" — mobile-friendly
    initial_sidebar_state="collapsed"
)

# ── CSS MOBILE-FIRST ──────────────────────────────────────────────
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Be Vietnam Pro', sans-serif !important; box-sizing: border-box; }
#MainMenu, header, footer { visibility: hidden; }

/* Mobile viewport fix */
.block-container {
    padding: 0.6rem 0.8rem !important;
    max-width: 100% !important;
}
.stApp { background: linear-gradient(135deg, #0D0D1A 0%, #1A1A2E 100%) !important; }

/* ── HEADER ── */
.buta-hdr {
    background: linear-gradient(135deg, #4C1D95, #7C3AED, #6D28D9);
    color: white; padding: 10px 16px; border-radius: 14px;
    margin-bottom: 12px; display: flex; justify-content: space-between;
    align-items: center; box-shadow: 0 4px 24px rgba(124,58,237,.45);
}
.buta-hdr h1 { margin: 0; font-size: 1.2rem; font-weight: 800; }
.buta-hdr small { opacity: .85; font-size: .72rem; }
.buta-time { font-size: 1.2rem; font-weight: 800; text-align:right; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #1A1A2E !important; border-radius: 12px; padding: 4px; gap: 4px;
    border: 1px solid #2D2D4E !important; overflow-x: auto;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; font-weight: 600 !important;
    color: #7C3AED !important; font-size: .85rem !important;
    white-space: nowrap !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7C3AED, #A855F7) !important; color: white !important;
}
.stTabs .stTabs [data-baseweb="tab-list"] { background: #111122 !important; border: 1px solid #2D2D4E !important; }
.stTabs .stTabs [data-baseweb="tab"] { color: #818CF8 !important; }
.stTabs .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #4338CA, #6366F1) !important; color: white !important; }

/* ── SECTION TITLE ── */
.sec-title {
    color: #A78BFA; font-size: .95rem; font-weight: 700;
    margin: 10px 0 8px; padding-bottom: 5px;
    border-bottom: 2px solid #3A3A5C;
}

/* ── DỊCH VỤ BUTTONS — dạng grid 2 cột responsive ── */
.dv-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px; margin-bottom: 10px;
}
.dv-btn {
    background: linear-gradient(145deg, #1A1A2E, #16213E);
    border: 1px solid #4C1D95; border-radius: 12px;
    padding: 10px 8px; text-align: center; cursor: pointer;
    transition: all .15s; color: white;
    -webkit-tap-highlight-color: transparent;
    touch-action: manipulation;
}
.dv-btn:active { background: linear-gradient(135deg, #5B21B6, #7C3AED); transform: scale(0.97); }
.dv-btn .name { font-size: .82rem; font-weight: 700; color: #C4B5FD; display: block; }
.dv-btn .price { font-size: .9rem; font-weight: 800; color: #A78BFA; display: block; margin-top:3px; }

/* ── CART ITEMS ── */
.cart-item {
    background: #1A1A2E; border: 1px solid #2D2D4E;
    border-radius: 10px; padding: 8px 12px; margin-bottom: 6px;
    display: flex; justify-content: space-between; align-items: center;
}
.cart-item .item-name { color: #C4B5FD; font-size: .85rem; font-weight: 600; flex: 1; }
.cart-item .item-price { color: #A78BFA; font-size: .9rem; font-weight: 700; margin: 0 8px; }
.cart-item .item-del {
    background: #3B1A1A; border: 1px solid #7F1D1D; color: #FCA5A5;
    border-radius: 6px; padding: 4px 8px; cursor: pointer; font-size: .8rem;
    touch-action: manipulation; -webkit-tap-highlight-color: transparent;
}

/* ── KPI CARDS — 2x2 trên mobile ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px; margin-bottom: 12px;
}
.kpi-card {
    background: linear-gradient(145deg, #1A1A2E, #16213E);
    border: 1px solid #2D2D4E; border-radius: 12px; padding: 12px;
    text-align: center;
}
.kpi-lbl { color: #818CF8; font-size: .65rem; font-weight: 700; text-transform: uppercase; letter-spacing: .8px; }
.kpi-val { color: #A78BFA; font-size: 1.15rem; font-weight: 800; margin-top: 4px; }

/* ── TỔNG TIỀN BOX ── */
.total-box {
    background: linear-gradient(135deg, #4C1D95, #7C3AED);
    color: white; border-radius: 14px; padding: 14px;
    text-align: center; margin: 8px 0;
    box-shadow: 0 4px 20px rgba(124,58,237,.4);
}
.total-box .lbl { font-size: .72rem; opacity: .85; }
.total-box .amt { font-size: 1.8rem; font-weight: 800; }

/* ── RECEIPT ── */
.receipt {
    font-family: 'Courier New', monospace !important;
    background: #1A1A2E; border: 2px dashed #4C1D95;
    border-radius: 12px; padding: 16px; max-width: 100%;
    margin: 0 auto; box-shadow: 0 6px 28px rgba(124,58,237,.3);
    color: #E0E0E0 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #7C3AED, #A855F7) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; font-weight: 700 !important;
    font-size: .9rem !important;
    box-shadow: 0 2px 10px rgba(124,58,237,.35) !important;
    min-height: 44px !important;          /* touch target iOS */
    touch-action: manipulation !important;
    -webkit-tap-highlight-color: transparent !important;
}
.stButton > button:active { opacity: .85 !important; }

/* ── INPUTS ── */
.stTextInput input, .stSelectbox select, .stNumberInput input {
    background: #1A1A2E !important; color: #E0E0E0 !important;
    border: 1px solid #3A3A5C !important; border-radius: 8px !important;
    font-size: 1rem !important; min-height: 44px !important;
}
.stSelectbox > div > div { background: #1A1A2E !important; color: #E0E0E0 !important; }

/* ── DATA EDITOR ── */
div[data-testid="stDataEditor"] { border-radius: 12px !important; overflow: hidden; }
div[data-testid="stDataEditor"] * { background-color: #1A1A2E !important; color: #E0E0E0 !important; }

/* ── MISC ── */
hr { border-color: #2D2D4E !important; }
div[data-testid="stInfo"]    { background: #1A1A3E !important; border-color: #4338CA !important; color: #A5B4FC !important; }
div[data-testid="stSuccess"] { background: #0D2B1E !important; border-color: #10B981 !important; color: #6EE7B7 !important; }
div[data-testid="stError"]   { background: #2B0D0D !important; border-color: #EF4444 !important; color: #FCA5A5 !important; }
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-thumb { background: #7C3AED; border-radius: 3px; }

/* ── MOBILE: viewport meta ── */
@media (max-width: 480px) {
    .buta-hdr h1 { font-size: 1rem; }
    .kpi-val { font-size: 1rem; }
    .total-box .amt { font-size: 1.5rem; }
}
</style>

<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
""", unsafe_allow_html=True)

# ── DB ───────────────────────────────────────────────────────────
DB = "buta_nail.db"
def conn(): return sqlite3.connect(DB, check_same_thread=False)

SCHEMA_VER = 2

def init_db():
    c = conn()
    c.execute("CREATE TABLE IF NOT EXISTS _SchemaVersion(ver INTEGER)")
    row = c.execute("SELECT ver FROM _SchemaVersion LIMIT 1").fetchone()
    current_ver = row[0] if row else 0

    if current_ver < SCHEMA_VER:
        c.executescript("""
        DROP TABLE IF EXISTS HoaDon;
        DROP TABLE IF EXISTS DichVu;
        DROP TABLE IF EXISTS KhachHang;
        DROP TABLE IF EXISTS NhanVien;
        DROP TABLE IF EXISTS _SchemaVersion;
        CREATE TABLE _SchemaVersion(ver INTEGER);
        CREATE TABLE NhanVien(ID INTEGER PRIMARY KEY AUTOINCREMENT, TenNhanVien TEXT NOT NULL);
        CREATE TABLE KhachHang(ID INTEGER PRIMARY KEY AUTOINCREMENT, TenKhach TEXT NOT NULL, SoDienThoai TEXT);
        CREATE TABLE DichVu(ID INTEGER PRIMARY KEY AUTOINCREMENT, TenDichVu TEXT NOT NULL, GiaTien INTEGER NOT NULL);
        CREATE TABLE HoaDon(
            ID INTEGER PRIMARY KEY AUTOINCREMENT, NgayTao TEXT,
            KhachHang_ID INTEGER, NhanVien_ID INTEGER,
            DichVu_IDs TEXT, TienTip INTEGER DEFAULT 0,
            GiamGia INTEGER DEFAULT 0, TongTien INTEGER,
            FOREIGN KEY(KhachHang_ID) REFERENCES KhachHang(ID),
            FOREIGN KEY(NhanVien_ID)  REFERENCES NhanVien(ID)
        );
        """)
        c.execute("INSERT INTO _SchemaVersion(ver) VALUES(?)", (SCHEMA_VER,))
        c.executemany("INSERT INTO NhanVien(TenNhanVien) VALUES(?)", [("Lan",), ("Hoa",)])
        c.executemany("INSERT INTO KhachHang(TenKhach,SoDienThoai) VALUES(?,?)", [
            ("Nguyễn Thị Mai", "0901234567"), ("Trần Thị Hà", "0912345678")])
        c.executemany("INSERT INTO DichVu(TenDichVu,GiaTien) VALUES(?,?)", [
            ("Sơn gel cơ bản", 150000), ("Nail art họa tiết", 250000),
            ("Tẩy gel + sơn mới", 200000), ("Spa tay ngâm dưỡng", 120000),
            ("Đắp bột acrylic", 350000), ("Sơn thường 2 tay", 80000)])
        c.commit()
    c.close()

init_db()

def qdf(sql, p=None):
    c = conn(); df = pd.read_sql(sql, c, params=p); c.close(); return df

def load_nv(): return qdf("SELECT * FROM NhanVien")
def load_kh(): return qdf("SELECT * FROM KhachHang")
def load_dv(): return qdf("SELECT * FROM DichVu")

def load_hd(days=30):
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    return qdf("""SELECT h.ID, h.NgayTao,
        COALESCE(k.TenKhach,'Vãng lai') TenKhach,
        COALESCE(n.TenNhanVien,'—') TenNhanVien,
        h.TienTip, h.GiamGia, h.TongTien
        FROM HoaDon h
        LEFT JOIN KhachHang k ON h.KhachHang_ID=k.ID
        LEFT JOIN NhanVien n ON h.NhanVien_ID=n.ID
        WHERE h.NgayTao>=? ORDER BY h.NgayTao DESC""", (since,))

def save_hd(kh_id, nv_id, dv_ids, tip, giam, tong):
    c = conn()
    c.execute("""INSERT INTO HoaDon(NgayTao,KhachHang_ID,NhanVien_ID,DichVu_IDs,TienTip,GiamGia,TongTien)
                 VALUES(?,?,?,?,?,?,?)""",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), kh_id, nv_id,
               json.dumps(dv_ids), tip, giam, tong))
    c.commit(); c.close()

def add_kh(ten, sdt):
    c = conn()
    c.execute("INSERT INTO KhachHang(TenKhach,SoDienThoai) VALUES(?,?)", (ten, sdt))
    c.commit(); c.close()

def save_table(df, table):
    df_save = df.drop(columns=["ID"], errors="ignore").copy()
    df_save = df_save.dropna(how="all")
    first_col = df_save.columns[0]
    df_save = df_save[df_save[first_col].notna() & (df_save[first_col].astype(str).str.strip() != "")]
    c = conn()
    c.execute(f"DELETE FROM {table}")
    if not df_save.empty:
        df_save.to_sql(table, c, if_exists="append", index=False)
    c.commit(); c.close()

# ── SESSION STATE ────────────────────────────────────────────────
for k, v in [("cart", []), ("show_bill", False), ("last_bill", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── HEADER ───────────────────────────────────────────────────────
now = datetime.now()
st.markdown(f"""<div class="buta-hdr">
<div><h1>💅 BUTA NAIL</h1><small>Luxury Pink Edition — POS</small></div>
<div><div class="buta-time">{now.strftime('%H:%M')}</div>
<small style="opacity:.8">{now.strftime('%d/%m/%Y')}</small></div>
</div>""", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🛒 Bán Hàng", "⚙️ Quản Lý", "📊 Báo Cáo"])

# ════════════════════════════════════════════════════════════════
# TAB 1 — BÁN HÀNG (single column, mobile-first)
# ════════════════════════════════════════════════════════════════
with tab1:
    dv_df = load_dv(); nv_df = load_nv(); kh_df = load_kh()

    # ── Chọn thợ & khách ──
    st.markdown('<div class="sec-title">👩 Thông Tin</div>', unsafe_allow_html=True)
    nv_opts = ["— Chọn thợ —"] + nv_df.TenNhanVien.tolist()
    kh_opts = ["— Khách vãng lai —"] + kh_df.TenKhach.tolist()
    sel_nv = st.selectbox("Thợ thực hiện", nv_opts, label_visibility="visible")
    sel_kh = st.selectbox("Khách hàng", kh_opts, label_visibility="visible")

    with st.expander("➕ Thêm khách hàng mới"):
        nk_ten = st.text_input("Tên khách", key="nk_ten")
        nk_sdt = st.text_input("Số điện thoại", key="nk_sdt")
        if st.button("💾 Lưu khách", key="btn_luu_kh"):
            if nk_ten:
                add_kh(nk_ten, nk_sdt)
                st.success(f"✅ Đã thêm {nk_ten}!")
                st.rerun()

    # ── Bảng giá dịch vụ — dạng HTML grid (touch-friendly) ──
    st.markdown('<div class="sec-title">💆 Chọn Dịch Vụ</div>', unsafe_allow_html=True)
    search = st.text_input("🔍 Tìm dịch vụ", placeholder="Gõ tên dịch vụ...", label_visibility="collapsed")
    filtered = dv_df[dv_df.TenDichVu.str.contains(search, case=False, na=False)] if search else dv_df

    # Chia 2 cột dùng st.columns — button có min-height 44px đủ touch target
    cols = st.columns(2, gap="small")
    for i, row in filtered.iterrows():
        with cols[i % 2]:
            if st.button(
                f"**{row.TenDichVu}**\n{row.GiaTien:,.0f}đ",
                key=f"dv_{row.ID}",
                use_container_width=True
            ):
                st.session_state.cart.append({
                    "id": int(row.ID), "ten": row.TenDichVu, "gia": int(row.GiaTien)
                })
                st.rerun()

    # ── Giỏ hàng ──
    st.markdown('<div class="sec-title">📋 Hóa Đơn</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.info("💡 Bấm dịch vụ bên trên để thêm vào hóa đơn")
    else:
        # Hiển thị từng item giỏ hàng
        for idx, item in enumerate(st.session_state.cart):
            c1, c2, c3 = st.columns([4, 3, 1], gap="small")
            c1.markdown(f"**{item['ten']}**")
            c2.markdown(
                f"<span style='color:#A78BFA;font-weight:700'>{item['gia']:,.0f}đ</span>",
                unsafe_allow_html=True
            )
            with c3:
                if st.button("✕", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx); st.rerun()

        st.divider()
        if st.button("🗑️ Xóa tất cả", use_container_width=True, key="btn_clear"):
            st.session_state.cart = []; st.rerun()

    # ── Tip & Giảm giá ──
    c1, c2 = st.columns(2, gap="small")
    tip  = c1.number_input("💝 Tiền Tip (đ)",   min_value=0, step=10000, value=0)
    giam = c2.number_input("🏷️ Giảm giá (đ)", min_value=0, step=10000, value=0)

    subtotal = sum(i["gia"] for i in st.session_state.cart)
    total    = max(0, subtotal + tip - giam)

    st.markdown(f"""<div class="total-box">
        <div class="lbl">TỔNG THANH TOÁN</div>
        <div class="amt">{total:,.0f}đ</div>
    </div>""", unsafe_allow_html=True)

    if st.button("💳  CHỐT BILL & IN HÓA ĐƠN", use_container_width=True, key="btn_checkout"):
        if not st.session_state.cart:
            st.error("⚠️ Chưa có dịch vụ!")
        else:
            nv_id = None; kh_id = None
            if sel_nv != "— Chọn thợ —":
                r = nv_df[nv_df.TenNhanVien == sel_nv]
                if not r.empty: nv_id = int(r.iloc[0].ID)
            if sel_kh != "— Khách vãng lai —":
                r = kh_df[kh_df.TenKhach == sel_kh]
                if not r.empty: kh_id = int(r.iloc[0].ID)
            save_hd(kh_id, nv_id, [i["id"] for i in st.session_state.cart], tip, giam, total)
            st.session_state.last_bill = {
                "nv": sel_nv, "kh": sel_kh,
                "items": st.session_state.cart.copy(),
                "tip": tip, "giam": giam, "sub": subtotal, "total": total,
                "time": now.strftime("%d/%m/%Y %H:%M")
            }
            st.session_state.show_bill = True
            st.session_state.cart = []
            st.rerun()

    # ── BILL RECEIPT ──
    if st.session_state.show_bill and st.session_state.last_bill:
        b = st.session_state.last_bill
        st.divider()
        rows_html = "".join(
            f"<div style='display:flex;justify-content:space-between;margin:3px 0;font-size:.85rem;color:#C4B5FD'>"
            f"<span>{i['ten']}</span><span>{i['gia']:,.0f}đ</span></div>"
            for i in b["items"]
        )
        giam_row = (f"<div style='display:flex;justify-content:space-between;color:#F87171'>"
                    f"<span>Giảm giá</span><span>-{b['giam']:,.0f}đ</span></div>") if b["giam"] else ""
        tip_row  = (f"<div style='display:flex;justify-content:space-between;color:#34D399'>"
                    f"<span>Tiền Tip 💝</span><span>+{b['tip']:,.0f}đ</span></div>") if b["tip"] else ""

        st.markdown(f"""<div class="receipt">
<div style="text-align:center;color:#A78BFA;font-weight:900;font-size:1.1rem">💅 BUTA NAIL 💅</div>
<div style="text-align:center;color:#818CF8;font-size:.7rem">Luxury Nail Salon</div>
<hr style="border:none;border-top:1px dashed #4C1D95;margin:8px 0">
<div style="font-size:.8rem;color:#E0E0E0">📅 {b['time']}</div>
<div style="font-size:.8rem;color:#E0E0E0">👩 Thợ: <b style='color:#C4B5FD'>{b['nv']}</b></div>
<div style="font-size:.8rem;color:#E0E0E0">👤 Khách: <b style='color:#C4B5FD'>{b['kh']}</b></div>
<hr style="border:none;border-top:1px dashed #4C1D95;margin:8px 0">
<div style="font-weight:700;color:#818CF8;font-size:.75rem;margin-bottom:4px">DỊCH VỤ</div>
{rows_html}
<hr style="border:none;border-top:1px dashed #4C1D95;margin:8px 0">
<div style="display:flex;justify-content:space-between;font-size:.85rem;color:#E0E0E0"><span>Tạm tính</span><span>{b['sub']:,.0f}đ</span></div>
{giam_row}{tip_row}
<hr style="border:none;border-top:1px dashed #4C1D95;margin:8px 0">
<div style="display:flex;justify-content:space-between;font-size:1.1rem;font-weight:900;color:#A78BFA">
<span>TỔNG CỘNG</span><span>{b['total']:,.0f}đ</span></div>
<hr style="border:none;border-top:1px dashed #4C1D95;margin:8px 0">
<div style="text-align:center;color:#818CF8;font-size:.75rem">Cảm ơn quý khách! 🌸<br>Hẹn gặp lại tại BUTA NAIL</div>
</div>""", unsafe_allow_html=True)

        if st.button("✅ Đóng hóa đơn", use_container_width=True, key="btn_close"):
            st.session_state.show_bill = False; st.rerun()

# ════════════════════════════════════════════════════════════════
# TAB 2 — QUẢN LÝ
# ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-title">⚙️ Quản Lý Dữ Liệu</div>', unsafe_allow_html=True)
    m1, m2, m3 = st.tabs(["👩 Nhân Viên", "👤 Khách Hàng", "💆 Bảng Giá"])

    with m1:
        nv_ed = st.data_editor(
            load_nv(), num_rows="dynamic", use_container_width=True, key="ed_nv",
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "TenNhanVien": st.column_config.TextColumn("Tên Nhân Viên", width="large")
            }
        )
        if st.button("💾 Lưu Nhân Viên", key="sv_nv", use_container_width=True):
            save_table(nv_ed, "NhanVien"); st.success("✅ Đã lưu!"); st.rerun()

    with m2:
        kh_ed = st.data_editor(
            load_kh(), num_rows="dynamic", use_container_width=True, key="ed_kh",
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "TenKhach": st.column_config.TextColumn("Tên Khách"),
                "SoDienThoai": st.column_config.TextColumn("Số Điện Thoại")
            }
        )
        if st.button("💾 Lưu Khách Hàng", key="sv_kh", use_container_width=True):
            save_table(kh_ed, "KhachHang"); st.success("✅ Đã lưu!"); st.rerun()

    with m3:
        dv_ed = st.data_editor(
            load_dv(), num_rows="dynamic", use_container_width=True, key="ed_dv",
            column_config={
                "ID": st.column_config.NumberColumn("ID", disabled=True),
                "TenDichVu": st.column_config.TextColumn("Tên Dịch Vụ", width="large"),
                "GiaTien": st.column_config.NumberColumn("Giá Tiền (đ)", format="%d")
            }
        )
        if st.button("💾 Lưu Bảng Giá", key="sv_dv", use_container_width=True):
            save_table(dv_ed, "DichVu"); st.success("✅ Đã lưu!"); st.rerun()

# ════════════════════════════════════════════════════════════════
# TAB 3 — BÁO CÁO (2x2 grid thay 4 cột)
# ════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-title">📊 Dashboard Doanh Thu</div>', unsafe_allow_html=True)
    hd_df = load_hd(30)
    today = datetime.now().strftime("%Y-%m-%d")

    dt_today = hd_df[hd_df.NgayTao.str.startswith(today)].TongTien.sum() if not hd_df.empty else 0
    dt_7ngay = hd_df[hd_df.NgayTao >= (datetime.now()-timedelta(days=7)).strftime("%Y-%m-%d")].TongTien.sum() if not hd_df.empty else 0
    so_bill  = len(hd_df)
    tb_bill  = hd_df.TongTien.mean() if not hd_df.empty else 0

    # ── KPI 2x2 grid ──
    st.markdown(f"""<div class="kpi-grid">
<div class="kpi-card"><div class="kpi-lbl">💰 Hôm Nay</div><div class="kpi-val">{dt_today:,.0f}đ</div></div>
<div class="kpi-card"><div class="kpi-lbl">📅 7 Ngày</div><div class="kpi-val">{dt_7ngay:,.0f}đ</div></div>
<div class="kpi-card"><div class="kpi-lbl">🧾 Tổng Bill</div><div class="kpi-val">{so_bill}</div></div>
<div class="kpi-card"><div class="kpi-lbl">📊 TB/Bill</div><div class="kpi-val">{tb_bill:,.0f}đ</div></div>
</div>""", unsafe_allow_html=True)

    if not hd_df.empty:
        hd_df["Ngay"] = hd_df.NgayTao.str[:10]
        daily = hd_df.groupby("Ngay").TongTien.sum().reset_index()

        fig = px.area(daily, x="Ngay", y="TongTien", title="📈 Doanh Thu 30 Ngày",
                      labels={"Ngay": "Ngày", "TongTien": "Doanh Thu (đ)"},
                      color_discrete_sequence=["#7C3AED"])
        fig.update_traces(fill="tozeroy", fillcolor="rgba(124,58,237,0.18)",
                          line_color="#A855F7", line_width=2.5)
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(26,26,46,0.8)",
            font_family="Be Vietnam Pro", font_color="#C4B5FD",
            title_font_color="#A78BFA", title_font_size=14,
            xaxis=dict(gridcolor="#2D2D4E", color="#818CF8"),
            yaxis=dict(gridcolor="#2D2D4E", color="#818CF8"),
            margin=dict(l=0, r=0, t=36, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Pie & Bar: full width trên mobile (không chia cột) ──
        by_nv = hd_df.groupby("TenNhanVien").TongTien.sum().reset_index()
        fig2 = px.pie(by_nv, names="TenNhanVien", values="TongTien", title="👩 Doanh Thu Theo Thợ",
                      color_discrete_sequence=["#7C3AED","#A855F7","#6366F1","#818CF8","#4C1D95"])
        fig2.update_traces(textfont_color="white")
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_family="Be Vietnam Pro",
            font_color="#C4B5FD", title_font_color="#A78BFA",
            legend=dict(font=dict(color="#C4B5FD")), margin=dict(l=0,r=0,t=36,b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)

        by_kh = hd_df.groupby("TenKhach").TongTien.sum().nlargest(8).reset_index()
        fig3 = px.bar(by_kh, x="TongTien", y="TenKhach", orientation="h",
                      title="🏆 Top Khách Hàng",
                      color="TongTien",
                      color_continuous_scale=["#4C1D95","#7C3AED","#A855F7"])
        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(26,26,46,0.8)",
            font_family="Be Vietnam Pro", font_color="#C4B5FD",
            title_font_color="#A78BFA", coloraxis_showscale=False,
            xaxis=dict(gridcolor="#2D2D4E", color="#818CF8"),
            yaxis=dict(gridcolor="#2D2D4E", color="#818CF8"),
            margin=dict(l=0, r=0, t=36, b=0)
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('<div class="sec-title">📋 Lịch Sử Giao Dịch</div>', unsafe_allow_html=True)
        st.dataframe(
            hd_df[["ID","NgayTao","TenKhach","TenNhanVien","TienTip","GiamGia","TongTien"]]
            .rename(columns={"NgayTao":"Ngày","TenKhach":"Khách","TenNhanVien":"Thợ",
                             "TienTip":"Tip","GiamGia":"Giảm","TongTien":"Tổng"}),
            use_container_width=True, hide_index=True
        )
    else:
        st.info("📭 Chưa có dữ liệu giao dịch. Hãy bán hàng đi đã!")
