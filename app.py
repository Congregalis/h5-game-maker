from pathlib import Path

import os
import streamlit as st
from agno.utils.string import hash_string_sha256
from game_generator import GameGenerator, SqliteStorage

st.set_page_config(
    page_title="HTML5 Game Generator",
    page_icon="🎮",
    layout="wide",
)


st.title("Game Generator")
# st.markdown("##### 🎮 powered by [Agno](https://github.com/agno-agi/agno)")


def main() -> None:
    with st.sidebar.expander("🔑 API Key Settings"):
        api_key = st.text_input(
            "Google API Key",
            type="password",
            help="Get your API Key from Google AI Studio",
            value=st.session_state.get("google_api_key", ""),
            key="api_key_input"
        )

    game_description_key = f"game_description_{st.session_state.get('game_description', 'default')}"
    game_description = st.sidebar.text_area(
        "🎮 Describe your game",
        value=st.session_state.get("game_description", 
            "An asteroids game. Make sure the asteroids move randomly and are random sizes."),
        height=100,
        key=game_description_key
    )

    generate_game = st.sidebar.button("Generate Game! 🚀")

    st.sidebar.markdown("## Example Games")
    example_games = [
        "A simple snake game where the snake grows longer as it eats food",
        "A breakout clone with colorful blocks and power-ups",
        "A space invaders game with multiple enemy types",
        "A simple platformer with jumping mechanics",
    ]

    for game in example_games:
        if st.sidebar.button(game):
            st.session_state["game_description"] = game
            game_description = game
            generate_game = True

    if generate_game:
        with st.spinner("Generating your game... This might take a minute..."):
            try:
                hash_of_description = hash_string_sha256(game_description)
                google_api_key = os.getenv("GOOGLE_API_KEY", "")
                if api_key is not None and api_key != "":
                    google_api_key = api_key
                game_generator = GameGenerator(
                    session_id=f"game-gen-{hash_of_description}",
                    storage=SqliteStorage(
                        table_name="game_generator_workflows",
                        db_file="tmp/workflows.db",
                    ),
                    google_api_key=google_api_key
                )

                result = list(game_generator.run(game_description=game_description))

                games_dir = Path(__file__).parent.joinpath("games")
                game_path = games_dir / "game_output_file.html"

                if game_path.exists():
                    game_code = game_path.read_text()

                    with st.status(
                        "Game Generated Successfully!", expanded=True
                    ) as status:
                        st.subheader("Play the Game")
                        st.components.v1.html(game_code, height=700, scrolling=False)

                        st.subheader("Game Instructions")
                        st.write(result[-1].content)
                        
                        st.download_button(
                            label="Download Game HTML",
                            data=game_code,
                            file_name="game.html",
                            mime="text/html",
                        )

                        status.update(
                            label="Game ready to play!",
                            state="complete",
                            expanded=True,
                        )
                    
                    st.subheader("Game Source Code")
                    with st.expander("Source Code", expanded=False):
                        # 添加下载源代码按钮并美化
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            st.download_button(
                                label="📥 Download",
                                data=game_code,
                                file_name="game_source.html",
                                mime="text/html",
                                use_container_width=True,
                                key=f"download_source_{hash_of_description}"  # 添加唯一key
                            )
                        st.markdown("---")  # 添加分隔线
                        st.code(game_code, language="html")

            except Exception as e:
                st.error(f"Failed to generate game: {str(e)}")

    st.sidebar.markdown("---")
    if st.sidebar.button("Restart"):
        st.rerun()


main()

# 在文件末尾添加页脚
st.markdown(
    """
    <div style='position: fixed; bottom: 0; right: 0; padding: 10px; font-size: 12px; color: #666;'>
        🎮 powered by <a href='https://github.com/agno-agi/agno' target='_blank'>Agno</a>
    </div>
    """,
    unsafe_allow_html=True
)