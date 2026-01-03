import streamlit as st
import pandas as pd
import numpy as np 

st.set_page_config(
    page_title="MOFC Assign",
    layout="wide"
)

st.title("MOFC Assign")

st.subheader("GlobalCfg")
cols = st.columns(4)
OPMODE_ENUM = {"SingleChannel": 0, "CommonQuad": 1, "CommonOctal": 2}

with cols[0]:
    opmode = st.selectbox("OpMode", list(OPMODE_ENUM))
with cols[1]:
    pm_pri = st.number_input("PM-PRI [us]", value=1000, step=1)
with cols[2]:
    pm_pw = st.number_input("PM-PW [us]", value=10, step=1)
with cols[3]:
    if st.button("Write GlobalCfg"):
        st.info(f"Writing GlobalCfg: {opmode}, PRI={pm_pri}, PW={pm_pw}")




st.subheader("BitConfig")
cols = st.columns(4)
with cols[0]:
    bit_lo_freq = st.number_input("BIT_LO_FREQ [MHz]", value=150)
with cols[1]:
    bit_out_pwr = st.selectbox("BIT_OUT_PWR [dBm]", np.arange(-30,-94,-1).tolist())
with cols[2]:
    bit_int_ext = st.selectbox("BIT INT/EXT", ["INT", "EXT"])
with cols[3]:
    bit_mode = st.selectbox("PLS / CW", ["PLS", "CW"])


st.divider()
st.subheader("ChannelsConfig")

# ==========================================================
# CENTER PANEL – CHANNELS CONFIGURATION
# ==========================================================



RFISRC_ENUM = {"ANT": 0, "BIT": 1}
RFIBS_ENUM = {"0.35-4.75": 0, "2-6": 1, "6-18": 2, "TERMINATED": 3}
IFOBS_ENUM = {"0.35-2.4": 0, "2.75-4.75": 1}

DCA_RANGE = list(np.arange(0,31.5,0.5))

TF_VSW = {"BYPASS": 0, "BAND1": 1, "BAND2": 2, "BAND3": 3}
TF_V_RANGE = list(range(16))


TF2_HPF_SW_ENUM = {"BYPASS": 0, "HPF_1": 1, "HPF_2": 2, "HPF_3": 3,"HPF_4": 4 }
TF2_LPF_SW_ENUM = {"BYPASS": 0, "LPF_1": 1, "LPF_2": 2, "LPF_3": 3,"LPF_4": 4 }
TF2_ST_RANGE = list(range(16))

channels = [f"Ch{i}" for i in range(1, 9)]
LO_FREQ_RANGE = np.arange(10000, 16750, 125).tolist()

df = pd.DataFrame({
    "RFISRC": [list(RFISRC_ENUM.keys())[0]] * 8,
    "RFIBS": [list(RFIBS_ENUM.keys())[0]] * 8,
    "IFOBS":  [list(IFOBS_ENUM.keys())[0]] * 8,
    "DCA1": [0] * 8,
    "DCA2": [0] * 8,
    "DCA3": [0] * 8,
    "TF1_VSW": [list(TF_VSW.keys())[0]] * 8,
    "TF1_VH": [0] * 8,
    "TF1_VL": [0] * 8,
    "TF3_VSW": [list(TF_VSW.keys())[0]] * 8,
    "TF3_VH": [0] * 8,
    "TF3_VL": [0] * 8,
    "TF2_HPF_SW": [list(TF2_HPF_SW_ENUM.keys())[0]] * 8,
    "TF2_HPF_ST": [0] * 8,
    "TF2_LPF_SW": [list(TF2_LPF_SW_ENUM.keys())[0]] * 8,
    "TF2_LPF_ST": [0] * 8,
    "LO_FREQ": [LO_FREQ_RANGE[0]] * 8,
    "LO_PDWN": [DCA_RANGE[0]] * 8,
}, index=channels)





# 1. Define your existing config dictionary first
config = {
    "RFISRC": st.column_config.SelectboxColumn("RFISRC", options=list(RFISRC_ENUM.keys())),
    "RFIBS": st.column_config.SelectboxColumn("RFIBS", options=list(RFIBS_ENUM.keys())),
    "IFOBS": st.column_config.SelectboxColumn("IFOBS", options=list(IFOBS_ENUM.keys())),
    "DCA1": st.column_config.SelectboxColumn("DCA1", options=DCA_RANGE),
    "DCA2": st.column_config.SelectboxColumn("DCA2", options=DCA_RANGE),
    "DCA3": st.column_config.SelectboxColumn("DCA3", options=DCA_RANGE),
    "TF1_VSW": st.column_config.SelectboxColumn("TF1_VSW", options=list(TF_VSW.keys())),
    "TF1_VH": st.column_config.SelectboxColumn("TF1_VH", options=TF_V_RANGE),
    "TF1_VL": st.column_config.SelectboxColumn("TF1_VL", options=TF_V_RANGE),
    "TF3_VSW": st.column_config.SelectboxColumn("TF3_VSW", options=list(TF_VSW.keys())),
    "TF3_VH": st.column_config.SelectboxColumn("TF3_VH", options=TF_V_RANGE),
    "TF3_VL": st.column_config.SelectboxColumn("TF3_VL", options=TF_V_RANGE),
    "TF2_HPF_SW": st.column_config.SelectboxColumn("TF2_HPF_SW", options=list(TF2_HPF_SW_ENUM.keys())),
    "TF2_HPF_ST": st.column_config.SelectboxColumn("TF2_HPF_ST", options=TF2_ST_RANGE),
    "TF2_LPF_SW": st.column_config.SelectboxColumn("TF2_LPF_SW", options=list(TF2_LPF_SW_ENUM.keys())),
    "TF2_LPF_ST": st.column_config.SelectboxColumn("TF2_LPF_ST", options=TF2_ST_RANGE),
    "LO_FREQ": st.column_config.SelectboxColumn("LO_FREQ", options=LO_FREQ_RANGE),
    "LO_PDWN": st.column_config.SelectboxColumn("LO_PDWN", options=[0, 1]),
}


# 3. Call the editor
edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed",
    column_config=config
)






# no_sort_config = {
#     col: st.column_config.Column(required=True) 
#     for col in df.columns
# }
# edited_df = st.data_editor(
#     df,
#     use_container_width=True,
#     num_rows="fixed",
#     column_config={
#         "RFISRC": st.column_config.SelectboxColumn(
#             "RFISRC",
#             options=list(RFISRC_ENUM.keys())
#         ),
#         "RFIBS": st.column_config.SelectboxColumn(
#             "RFIBS",
#             options=list(RFIBS_ENUM.keys())
#         ),
#         "IFOBS": st.column_config.SelectboxColumn(
#             "IFOBS",
#             options=list(IFOBS_ENUM.keys())
#         ),        
#         "DCA1": st.column_config.SelectboxColumn(
#             "DCA1",
#             options=DCA_RANGE
#         ),     
#         "TF1_VSW": st.column_config.SelectboxColumn(
#             "TF1_VSW",
#             options=list(TF_VSW.keys())
#         ),     
#         "TF1_VH": st.column_config.SelectboxColumn(
#             "TF1_VL",
#             options=TF_V_RANGE
#         ),           

#         "TF1_VL": st.column_config.SelectboxColumn(
#             "TF1_VL",
#             options=TF_V_RANGE
#         ),           
#         "TF3_VSW": st.column_config.SelectboxColumn(
#             "TF3_VSW",
#             options=list(TF_VSW.keys())
#         ),     
#         "TF3_VH": st.column_config.SelectboxColumn(
#             "TF3_VL",
#             options=TF_V_RANGE
#         ),           

#         "TF3_VL": st.column_config.SelectboxColumn(
#             "TF3_VL",
#             options=TF_V_RANGE
#         ),           
#         "LO_FREQ": st.column_config.SelectboxColumn(
#             "LO_FREQ",
#             options=LO_FREQ_RANGE#[10000,20000]
#         ),           

#         "LO_PDWN": st.column_config.SelectboxColumn(
#             "LO_PDWN",
#             options=[0,1]
#         ),           



#         }
# )

write_checksum = st.checkbox(
    "Write Checksum", 
    value=False, 
    help="Check this to include a checksum for the entire data batch."
)
if st.button("SendConfigMessage", type="primary"):
    st.write("This is a primary action button.")
if st.button("SendLoadRfSetup", type="primary"):
        st.write("This is a primary action button.")












# ==========================================================
# STATUS BAR
# ==========================================================
# st.divider()

# status_cols = st.columns(8)

# status_cols[0].metric("Temperature", "46°C")
# status_cols[1].metric("AGC", "Good")
# status_cols[2].metric("CLK_STAT", "OK")
# status_cols[3].metric("RF_READY", "1")
# status_cols[4].metric("RSVD", "0")
# status_cols[5].metric("LO2_LCK", "1")
# status_cols[6].metric("FPGA Ver", "3.5.4.6")
# status_cols[7].metric("Serial Num", "5.a")

# ==========================================================
# REGISTER READ / WRITE
# ==========================================================
st.divider()
st.subheader("Global Read / Write regs")

rw_col1, rw_col2 = st.columns(2)

with rw_col1:
    st.markdown("### Read Reg")
    read_addr = st.number_input("Addr (Read)", min_value=0, step=1)
    if st.button("Read Reg"):
        st.success(f"Read Addr {read_addr}: 0x33")

with rw_col2:
    st.markdown("### Write Reg")
    write_addr = st.number_input("Addr (Write)", min_value=0, step=1)
    write_data = st.text_input("WriteData (hex)", "0x44")
    if st.button("Write Reg"):
        st.success(f"Wrote {write_data} to Addr {write_addr}")
