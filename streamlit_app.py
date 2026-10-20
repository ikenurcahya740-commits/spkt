import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
) import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# Config Halaman
st.set_page_config(
    page_title="Visualisasi 3D AAS GBC Avanta & Modul Analisis",
    page_icon="🔬",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .stCard {
        background-color: #f8fafc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Aplikasi Simulator & Analisis Spektrofotometer Serapan Atom (AAS)</div>", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "📦 Model 3D AAS GBC-Avanta (1:1)", 
    "📊 Kurva Kalibrasi & Hitung Konsentrasi", 
    "🧪 Mekanisme Interferensi Ca & Pembebas (3D)"
])

# ==========================================
# TAB 1: 3D MODEL AAS GBC AVANTA INTERAKTIF
# ==========================================
with tab1:
    st.header("Visualisasi 3D Interaktif AAS GBC-Avanta")
    st.write("Klik pada komponen 3D instrumen untuk melihat fungsi dan detail komponennya.")
    
    col_view, col_info = st.columns([2, 1])
    
    with col_view:
        # High-performance Three.js Interactive AAS 3D Model
        three_js_code = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { margin: 0; overflow: hidden; background-color: #1e1e1e; font-family: sans-serif; }
                #canvas-container { width: 100vw; height: 500px; }
                #info-overlay {
                    position: absolute;
                    bottom: 10px;
                    left: 10px;
                    color: white;
                    background: rgba(0,0,0,0.7);
                    padding: 8px 12px;
                    border-radius: 5px;
                    font-size: 12px;
                    pointer-events: none;
                }
            </style>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        </head>
        <body>
            <div id="canvas-container"></div>
            <div id="info-overlay">Gunakan Klik-Kiri untuk Putar, Scroll untuk Zoom, Klik Komponen untuk Detail</div>

            <script>
                const container = document.getElementById('canvas-container');
                const scene = new THREE.Scene();
                scene.background = new THREE.Color(0x22222b);

                const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
                camera.position.set(0, 40, 100);

                const renderer = new THREE.WebGLRenderer({ antialias: true });
                renderer.setSize(container.clientWidth, container.clientHeight);
                renderer.shadowMap.enabled = true;
                container.appendChild(renderer.domElement);

                const controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;

                // Lighting
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
                scene.add(ambientLight);

                const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
                dirLight.position.set(50, 80, 50);
                dirLight.castShadow = true;
                scene.add(dirLight);

                // AAS GBC Avanta Scale 1:1 Assembly (Approx 96cm x 61cm x 53cm)
                const aasGroup = new THREE.Group();

                // 1. Main Chassis Body
                const bodyGeo = new THREE.BoxGeometry(96, 53, 61);
                const bodyMat = new THREE.MeshStandardMaterial({ color: 0xe0e0e0, roughness: 0.3 });
                const mainBody = new THREE.Mesh(bodyGeo, bodyMat);
                mainBody.position.set(0, 26.5, 0);
                mainBody.userData = { name: "Bodi Utama AAS GBC-Avanta", key: "chassis" };
                aasGroup.add(mainBody);

                // 2. Hollow Cathode Lamp Turret (Left side)
                const turretGeo = new THREE.CylinderGeometry(12, 12, 35, 32);
                const turretMat = new THREE.MeshStandardMaterial({ color: 0x333333, metalness: 0.5 });
                const turret = new THREE.Mesh(turretGeo, turretMat);
                turret.position.set(-30, 30, -5);
                turret.userData = { name: "Turret Lampu Katoda Rongga (HCL)", key: "hcl" };
                aasGroup.add(turret);

                // Lamps inside turret
                for(let i=0; i<8; i++) {
                    const angle = (i / 8) * Math.PI * 2;
                    const lampGeo = new THREE.CylinderGeometry(2, 2, 15, 16);
                    const lampMat = new THREE.MeshStandardMaterial({ color: 0xffa500, emissive: 0x331100 });
                    const lamp = new THREE.Mesh(lampGeo, lampMat);
                    lamp.position.set(-30 + Math.cos(angle)*8, 30, -5 + Math.sin(angle)*8);
                    lamp.userData = { name: "Lampu Katoda Rongga (HCL)", key: "hcl" };
                    aasGroup.add(lamp);
                }

                // 3. Atomizer & Burner Compartment (Center Open Area)
                const chamberGeo = new THREE.BoxGeometry(30, 25, 25);
                const chamberMat = new THREE.MeshStandardMaterial({ color: 0x111111 });
                const chamber = new THREE.Mesh(chamberGeo, chamberMat);
                chamber.position.set(5, 25, 18);
                chamber.userData = { name: "Ruang Atomisasi / Kompartemen Burner", key: "atomizer" };
                aasGroup.add(chamber);

                // Titanium Burner Head
                const burnerGeo = new THREE.BoxGeometry(12, 6, 4);
                const burnerMat = new THREE.MeshStandardMaterial({ color: 0x888888, metalness: 0.8, roughness: 0.2 });
                const burner = new THREE.Mesh(burnerGeo, burnerMat);
                burner.position.set(5, 20, 18);
                burner.userData = { name: "Titanium Burner Head", key: "burner" };
                aasGroup.add(burner);

                // Flame Effect
                const flameGeo = new THREE.ConeGeometry(5, 12, 16);
                const flameMat = new THREE.MeshBasicMaterial({ color: 0x00ccff, transparent: true, opacity: 0.7 });
                const flame = new THREE.Mesh(flameGeo, flameMat);
                flame.position.set(5, 29, 18);
                flame.userData = { name: "Nyala Api Atomisasi (Air-Acetylene / N2O-Acetylene)", key: "flame" };
                aasGroup.add(flame);

                // Nebulizer & Spray Chamber Assembly
                const nebGeo = new THREE.CylinderGeometry(3, 3, 14, 16);
                nebGeo.rotateZ(Math.PI / 2);
                const nebMat = new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 });
                const neb = new THREE.Mesh(nebGeo, nebMat);
                neb.position.set(5, 10, 18);
                neb.userData = { name: "Nebulizer & Spray Chamber Polypropylene", key: "nebulizer" };
                aasGroup.add(neb);

                // Monochromator / Optics Box (Right)
                const monoGeo = new THREE.BoxGeometry(25, 20, 30);
                const monoMat = new THREE.MeshStandardMaterial({ color: 0x444444 });
                const mono = new THREE.Mesh(monoGeo, monoMat);
                mono.position.set(32, 26, -5);
                mono.userData = { name: "Monokromator Czerny-Turner", key: "monochromator" };
                aasGroup.add(mono);

                scene.add(aasGroup);

                // Raycasting for Interactivity
                const raycaster = new THREE.Raycaster();
                const mouse = new THREE.Vector2();

                window.addEventListener('click', (event) => {
                    const rect = renderer.domElement.getBoundingClientRect();
                    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

                    raycaster.setFromCamera(mouse, camera);
                    const intersects = raycaster.intersectObjects(aasGroup.children);

                    if (intersects.length > 0) {
                        const hitObject = intersects[0].object;
                        if(hitObject.userData && hitObject.userData.key) {
                            window.parent.postMessage({
                                type: 'AAS_COMPONENT_CLICK',
                                key: hitObject.userData.key
                            }, '*');
                        }
                    }
                });

                // Animation Loop
                function animate() {
                    requestAnimationFrame(animate);
                    controls.update();
                    flame.scale.y = 1 + Math.sin(Date.now() * 0.01) * 0.1; // Flame flicker effect
                    renderer.render(scene, camera);
                }
                animate();

                // Responsive Window
                window.addEventListener('resize', () => {
                    camera.aspect = container.clientWidth / container.clientHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(container.clientWidth, container.clientHeight);
                });
            </script>
        </body>
        </html>
        """
        components.html(three_js_code, height=520)

    with col_info:
        st.subheader("Detail Komponen")
        
        # Dictionary Informasi Komponen GBC-Avanta
        details = {
            "hcl": {
                "title": "Lampu Katoda Rongga (Hollow Cathode Lamp / HCL)",
                "desc": "Sumber radiasi resonansi spektral spesifik untuk unsur yang dianalisis. GBC Avanta dilengkapi dengan otomatisasi 8-lamp turret yang dapat berputar dan meluruskan posisi optik secara presisi."
            },
            "burner": {
                "title": "Burner Head (Kepala Pembakar)",
                "desc": "Terbuat dari bahan Titanium tahan korosi. Berfungsi menghasilkan nyala api yang stabil dan homogen tempat terjadinya desolvasi dan atomisasi sampel analit."
            },
            "atomizer": {
                "title": "Sistem Atomisasi (Atomizer)",
                "desc": "Mengubah larutan analit menjadi atom-atom bebas dalam tingkat energi dasar (ground state) agar dapat menyerap radiasi cahaya dari HCL."
            },
            "nebulizer": {
                "title": "Nebulizer & Spray Chamber",
                "desc": "Nebulizer memecah sampel cair menjadi aerosol halus menggunakan aliran gas bertekanan. Spray chamber menyaring tetesan aerosol besar sehingga hanya kabut sangat halus yang masuk ke nyala api."
            },
            "monochromator": {
                "title": "Monokromator Czerny-Turner",
                "desc": "Sistem optik kisi difraksi (holographic grating 1800 lines/mm) yang mengisolasi garis spektrum analit spesifik dari emisi lain sebelum ditangkap detektor PMT (Photomultiplier Tube)."
            },
            "flame": {
                "title": "Nyala Api (Flame System)",
                "desc": "Menggunakan campuran gas Udara-Asetilen (suhu ~2300°C) atau N2O-Asetilen (suhu ~2900°C untuk elemen refraktori)."
            },
            "chassis": {
                "title": "Bodi Utama AAS GBC-Avanta",
                "desc": "Dimensi nyata 1:1 (~96 x 61 x 53 cm). Mengakomodasi modul kendali gas otomatis, optik ganda (Double Beam), serta elektronik pemproses sinyal."
            }
        }

        # Pilih manual atau lewat interaksi
        selected_key = st.selectbox(
            "Atau pilih komponen dari daftar:",
            options=list(details.keys()),
            format_func=lambda x: details[x]["title"]
        )

        st.info(f"**{details[selected_key]['title']}**")
        st.write(details[selected_key]["desc"])

# ==========================================
# TAB 2: KALKULATOR REGRESI & ANALISIS SAMPLE
# ==========================================
with tab2:
    st.header("Kurva Kalibrasi & Penentuan Konsentrasi Sampel")
    
    col_input, col_graph = st.columns([1, 1.2])
    
    with col_input:
        st.subheader("1. Masukkan Data Deret Standar")
        
        # Default Data Frame
        default_data = pd.DataFrame({
            "Konsentrasi (ppm)": [0.0, 2.0, 4.0, 6.0, 8.0, 10.0],
            "Absorbansi": [0.000, 0.125, 0.248, 0.371, 0.490, 0.612]
        })
        
        edited_df = st.data_editor(
            default_data, 
            num_rows="dynamic",
            use_container_width=True,
            key="calibration_table"
        )
        
        # Hitung Regresi Linier
        x = edited_df["Konsentrasi (ppm)"].values
        y = edited_df["Absorbansi"].values
        
        if len(x) >= 2:
            # Regresi y = mx + c
            m, c = np.polyfit(x, y, 1)
            
            # Hitung R^2 (Koefisien Determinasi) & r (Koefisien Korelasi)
            y_pred = m * x + c
            correlation_matrix = np.corrcoef(x, y)
            r = correlation_matrix[0, 1]
            r_squared = r**2
            
            st.success("**Hasil Kurva Kalibrasi:**")
            st.latex(rf"y = {m:.5f}x + {c:.5f}")
            st.write(f"**Koefisien Korelasi ($r$):** `{r:.5f}`")
            st.write(f"**Koefisien Determinasi ($R^2$):** `{r_squared:.5f}`")
            
            st.divider()
            st.subheader("2. Hitung Konsentrasi Sampel")
            abs_sample = st.number_input("Masukkan Nilai Absorbansi Sampel (A):", min_value=0.0, max_value=2.0, value=0.310, step=0.001)
            
            # x = (y - c) / m
            if m != 0:
                conc_sample = (abs_sample - c) / m
                st.metric(label="Konsentrasi Sampel Terhitung", value=f"{conc_sample:.4f} ppm")
            else:
                st.error("Kemiringan (m) berharga 0, tidak dapat melakukan pembagian.")
        else:
            st.warning("Masukkan minimal 2 titik data untuk membentuk persamaan regresi.")

    with col_graph:
        st.subheader("Grafik Regresi Linier")
        if len(x) >= 2:
            fig = px.scatter(
                edited_df, x="Konsentrasi (ppm)", y="Absorbansi",
                title="Kurva Kalibrasi AAS",
                labels={"Konsentrasi (ppm)": "Konsentrasi (ppm)", "Absorbansi": "Absorbansi (A)"},
                trendline="ols",
                trendline_color_override="red"
            )
            fig.update_traces(marker=dict(size=10, color='blue'))
            
            # Tambahkan Titik Sampel jika ada
            if 'conc_sample' in locals():
                fig.add_trace(go.Scatter(
                    x=[conc_sample],
                    y=[abs_sample],
                    mode='markers',
                    marker=dict(color='green', size=14, symbol='star'),
                    name='Sampel Unknown'
                ))
            
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 3: VISUALISASI MEKANISME INTERFERENSI Ca
# ==========================================
with tab3:
    st.header("Simulasi Mekanisme Pembentukan Kompleks & Eliminasi Gangguan Analisis Kalsium (Ca)")
    
    st.markdown("""
    Dalam analisis Kalsium (Ca) menggunakan AAS nyala Udara-Asetilen, sering terjadi **Interferensi Kimia** akibat hadirnya anion seperti **Fosfat ($\text{PO}_4^{3-}$)**. 
    Fosfat bereaksi dengan Kalsium membentuk senyawa refraktori $\text{Ca}_3(\text{PO}_4)_2$ yang sukar teratomisasi pada suhu api, menyebabkan penurunan sinyal absorbansi secara signifikan.
    """)
    
    reagent = st.selectbox(
        "Pilih Reagen Pembebas / Pengkelat yang Ditambahkan:",
        ["Tanpa Reagen (Terjadi Gangguan Fosfat)", "Lantanum (La3+)", "Stronsium (Sr2+)", "EDTA"]
    )
    
    col_3d_chem, col_chem_text = st.columns([1.5, 1])
    
    with col_3d_chem:
        # Visualisasi Simulasi Atom/Molekul 3D
        chem_sim_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
            <style>body {{ margin: 0; background: #0f172a; }} canvas {{ width: 100%; height: 400px; }}</style>
        </head>
        <body>
            <script>
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(45, window.innerWidth / 400, 0.1, 1000);
                camera.position.z = 25;

                const renderer = new THREE.WebGLRenderer({{ antialias: true }});
                renderer.setSize(window.innerWidth, 400);
                document.body.appendChild(renderer.domElement);

                const light = new THREE.DirectionalLight(0xffffff, 1);
                light.position.set(10, 20, 10);
                scene.add(light);
                scene.add(new THREE.AmbientLight(0x555555));

                const group = new THREE.Group();

                // Create Spheres based on selection
                const mode = "{reagent}";

                if (mode.includes("Tanpa Reagen")) {{
                    // Stable Ca3(PO4)2 Refractory Matrix (Ca = Orange, PO4 = Purple)
                    for(let i=0; i<3; i++) {{
                        const ca = new THREE.Mesh(new THREE.SphereGeometry(1.2, 32, 32), new THREE.MeshStandardMaterial({{color: 0xffa500}}));
                        ca.position.set(-4 + i*4, 0, 0);
                        group.add(ca);
                    }}
                    for(let j=0; j<2; j++) {{
                        const po4 = new THREE.Mesh(new THREE.SphereGeometry(2.0, 32, 32), new THREE.MeshStandardMaterial({{color: 0x8a2be2}}));
                        po4.position.set(-2 + j*4, 3, 0);
                        group.add(po4);
                    }}
                }} else if (mode.includes("La3+") || mode.includes("Sr2+")) {{
                    // Releasing Agent (La/Sr binds PO4 preferentially, freeing Ca)
                    const caFree = new THREE.Mesh(new THREE.SphereGeometry(1.2, 32, 32), new THREE.MeshStandardMaterial({{color: 0xffa500}}));
                    caFree.position.set(-6, 0, 0); // Free Ca atom (Ready for absorption)
                    group.add(caFree);

                    // La/Sr Phosphate Complex
                    const releasingAtom = new THREE.Mesh(new THREE.SphereGeometry(1.8, 32, 32), new THREE.MeshStandardMaterial({{color: 0x00ffcc}}));
                    releasingAtom.position.set(2, 0, 0);
                    const po4 = new THREE.Mesh(new THREE.SphereGeometry(2.0, 32, 32), new THREE.MeshStandardMaterial({{color: 0x8a2be2}}));
                    po4.position.set(2, 3, 0);
                    group.add(releasingAtom);
                    group.add(po4);
                }} else {{
                    // EDTA Protective Chelating Agent
                    const caAtom = new THREE.Mesh(new THREE.SphereGeometry(1.2, 32, 32), new THREE.MeshStandardMaterial({{color: 0xffa500}}));
                    group.add(caAtom);
                    
                    // EDTA Ring Cage Structure
                    const torus = new THREE.Mesh(new THREE.TorusGeometry(3, 0.5, 16, 100), new THREE.MeshStandardMaterial({{color: 0x00ff00}}));
                    group.add(torus);
                }}

                scene.add(group);

                function animate() {{
                    requestAnimationFrame(animate);
                    group.rotation.x += 0.01;
                    group.rotation.y += 0.01;
                    renderer.render(scene, camera);
                }}
                animate();
            </script>
        </body>
        </html>
        """
        components.html(chem_sim_code, height=410)

    with col_chem_text:
        st.subheader("Penjelasan Reaksi Kimia")
        
        if "Tanpa Reagen" in reagent:
            st.error("❌ **Terjadi Interferensi Kimia**")
            st.markdown("""
            **Reaksi:**
            $$3\text{Ca}^{2+} + 2\text{PO}_4^{3-} \rightarrow \text{Ca}_3(\text{PO}_4)_2 \text{ (s)}$$
            
            Kalsium fosfat bersifat thermostable (refraktori) dan tidak terurai sempurna pada nyala udara-asetilen (~2300°C), sehingga jumlah atom $\text{Ca}^0$ bebas berkurang dan absorbansi turun drastic.
            """)
        elif "La3+" in reagent or "Sr2+" in reagent:
            st.success("✅ **Mekanisme Releasing Agent (Agen Pembebas)**")
            st.markdown(f"""
            **Reaksi dengan {reagent}:**
            $$\text{Ca}_3(\text{PO}_4)_2 + 2\text{La}^{3+} \rightarrow 2\text{LaPO}_4 \downarrow + 3\text{Ca}^{2+}$$
            
            - **Prinsip Kerja:** Kation $\text{La}^{3+}$ atau $\text{Sr}^{2+}$ membentuk ikatan yang jauh lebih stabil dengan anion $\text{PO}_4^{3-}$ dibanding Ca.
            - Kation ini 'merebut' fosfat, sehingga membebaskan ion $\text{Ca}^{2+}$ agar mudah teratomisasi menjadi atom netral $\text{Ca}^0$ di nyala api.
            """)
        else:
            st.success("✅ **Mekanisme Protective Chelating Agent (Agen Pengkelat Protektif)**")
            st.markdown("""
            **Reaksi dengan EDTA:**
            $$\text{Ca}^{2+} + \text{EDTA}^{4-} \rightarrow [\text{Ca-EDTA}]^{2-}$$
            
            - **Prinsip Kerja:** EDTA mengikat ion $\text{Ca}^{2+}$ membentuk kompleks kelat bermuatan yang stabil di fase larutan.
            - Hal ini **mencegah** $\text{Ca}^{2+}$ bereaksi dengan $\text{PO}_4^{3-}$. 
            - Saat memasuki nyala api, kompleks organic $[\text{Ca-EDTA}]^{2-}$ sangat mudah hancur/terbakar, membebaskan $\text{Ca}^0$ secara sempurna.
            """)
                
