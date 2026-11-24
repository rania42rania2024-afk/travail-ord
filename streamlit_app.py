
import streamlit as st
import runpy
import contextlib
import io
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Ordonnancement Q5-Q6", layout="wide")

st.title("Travaux pratiques d'ordonnancement")
st.subheader("Exécution des algorithmes Q5 et Q6")

st.write("Cliquez sur le bouton pour lancer le programme Python.")

if st.button("Exécuter Q5 et Q6"):
    sortie = io.StringIO()

    def afficher_graphique():
        fig = plt.gcf()
        st.pyplot(fig)
        plt.close(fig)

    ancien_show = plt.show
    plt.show = afficher_graphique

    try:
        with contextlib.redirect_stdout(sortie):
            runpy.run_path(
                str(Path(__file__).with_name("app.py")),
                run_name="__main__"
            )

        st.success("Exécution terminée avec succès.")
        st.text_area(
            "Résultats du programme",
            sortie.getvalue(),
            height=400
        )

    except Exception as e:
        st.error(f"Erreur : {e}")

    finally:
        plt.show = ancien_show
