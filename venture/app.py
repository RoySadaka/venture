from venture.config import Config
from venture.metadata import Metadata
import gradio as gr
from venture.config import Config
import venture.logic as lo
import venture.casual_utils as casual_utils 
import openai

class Venture:
    def __init__(self, openai_api_key:str, captain_email:str='', extra_role:str='', share:bool=False):
        Config.OPEN_AI_KEY = openai_api_key
        Config.CAPTAIN_EMAIL = captain_email
        Config.EXTRA_ROLE = extra_role
        self.share = share

    metadata: Metadata = Metadata()

    def get_all_elements(self):
        gr_elements = {e: gr.update(visible=True) for e in self.gr_elements}

        # VENTURE
        gr_elements[self.gr_venture_response].update(value=self.metadata.explore_llm_output.response_text)
        self.metadata.explore_last_picked_file_names = lo.get_updated_picked_docs(self.metadata)
        gr_elements[self.gr_doc_picker].update(value=self.metadata.explore_last_picked_file_names, choices=lo.get_doc_picker_all_choices(self.metadata))
        
        # COSMOS
        gr_elements[self.gr_delete_doc_picker].update(value=[], choices=self.metadata.file_names)
        gr_elements[self.gr_cosmos_textbox].update(value=self.metadata.cosmos_result)
        gr_elements[self.gr_file_upload].update(value=None)

        # INTERLINK
        gr_elements[self.gr_interlink_textbox].update(value=self.metadata.interlink_last_text, lines=len(self.metadata.interlink_last_text.split('\n')))
        lo.update_interlink_captain_details(self.metadata)
        gr_elements[self.gr_captain_details_textbox].update(visible=lo.get_captain_details_textbox_visibility(self.metadata), value=lo.get_captain_details_textbox_text(self.metadata))

        # CASUAL DETAILS
        gr_elements[self.gr_casual_details].update(value=casual_utils.get_casual_details(self.metadata))

        return gr_elements

    def call_llm_handler(self, user_query, picked_doc_file_names):
        picked_doc_file_names = set(picked_doc_file_names)
        self.metadata.explore_last_picked_file_names = picked_doc_file_names
        self.metadata.explore_llm_output = lo.call_llm(self.metadata, user_query)

        self.metadata.interlink_last_text = lo.get_interlink_message(self.metadata, user_query)
        return self.get_all_elements()

    def cosmos_index_handler(self, file_paths_to_upload, file_names_to_delete):
        lo.index_cosmos(self.metadata, file_paths_to_upload, file_names_to_delete)
        return self.get_all_elements()

    def dispatch_handler(self, contact_us_textbox):
        self.metadata.interlink_last_text = contact_us_textbox
        lo.invoke_email_draft(self.metadata, contact_us_textbox)
        return self.get_all_elements()

    def initialize(self):
        openai.api_key = Config.OPEN_AI_KEY
        self.gr_elements = []

        casual_utils.ensure_folder_created(Config.DOCUMENTATION_PATH)
        casual_utils.ensure_folder_created(Config.INDEX_PATH)

        lo.load_initial_metadata(self.metadata)
        self.metadata.sum_cost_in_since_start_session    = 0
        self.metadata.sum_cost_out_since_start_session   = 0
        
    def launch(self):
        self.initialize()

        # NAVIGATION TABS
        self.gr_explore_tab = gr.Tab("🧑‍🚀 Explore")
        self.gr_elements.append(self.gr_explore_tab)
        self.gr_cosmos_tab = gr.Tab("🌟 Cosmos")
        self.gr_elements.append(self.gr_cosmos_tab)
        self.gr_interlink_tab = gr.Tab("📡 Interlink")
        self.gr_elements.append(self.gr_interlink_tab)
        self.gr_codex_tab = gr.Tab("💫 Codex")
        self.gr_elements.append(self.gr_codex_tab)


        #--------------[EXPLORE]--------------#

        # EXPLORE HEADER
        self.gr_explore_media = gr.Markdown("""![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/app/explore.png)""")
        self.gr_elements.append(self.gr_explore_media)

        ## QUESTION
        self.gr_query_text = gr.Textbox(label='🧑‍🚀 Explorer', placeholder="Greetings explorer! Unleash your curiosity and let the docs reveal some wonders", lines=2, interactive=True, visible=True) # 2 for multiline
        self.gr_elements.append(self.gr_query_text)

        ## DROP DOWN
        self.gr_doc_picker = gr.Dropdown(choices=[Config.AUTO_PILOT_NAME]+self.metadata.file_names, value=[Config.AUTO_PILOT_NAME], multiselect=True, max_choices=Config.MAX_DOCS_TO_USE_AS_CONTEXT, label="📌 Cosmos", info="Currently, you can select up to 2 destinations; In 'Auto-Pilot' mode, Venture will plot the course", interactive=True, visible=True)
        self.gr_elements.append(self.gr_doc_picker)

        ## RUN BUTTON
        self.gr_call_llm_btn = gr.Button(value="🚀 Embark", interactive=True, visible=True)
        self.gr_elements.append(self.gr_call_llm_btn)

        ## ASSISTANT
        self.gr_venture_response = gr.Textbox(label='🌔 Venture', placeholder="✨ Stars of insights will be revealed here", interactive=False, visible=True)
        self.gr_elements.append(self.gr_venture_response)

        #--------------[INTERLINK]--------------#

        # INTERLINK HEADER
        self.gr_interlink_media = gr.Markdown(f"""![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/app/interlink.png)""")
        self.gr_elements.append(self.gr_interlink_media)
        
        self.gr_interlink_textbox = gr.Textbox(label='📡 Interlink', placeholder="Galactic aid at your service", lines=10, interactive=True, visible=True)
        self.gr_elements.append(self.gr_interlink_textbox)

        self.gr_captain_details_textbox = gr.Textbox(label='🧑‍✈️ Captain details', lines=2, interactive=False, visible=lo.get_captain_details_textbox_visibility(self.metadata), value=lo.get_captain_details_textbox_text(self.metadata))
        self.gr_elements.append(self.gr_captain_details_textbox)

        #--------------[COSMOS]--------------#

        # COSMOS HEADER
        self.gr_cosmos_media = gr.Markdown(f"""![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/app/cosmos.png)""")
        self.gr_elements.append(self.gr_cosmos_media)

        # COSMOS FILE UPLOAD
        self.gr_file_upload = gr.File(label='✨ Expand', file_count='multiple', file_types=lo.get_supported_file_types_suffixes())
        self.gr_elements.append(self.gr_file_upload)

        ## COSMOS DROP DOWN
        self.gr_delete_doc_picker = gr.Dropdown(label="💢 Annihilate", choices=self.metadata.file_names, multiselect=True, info="Identify files for removal", interactive=True, visible=True)
        self.gr_elements.append(self.gr_delete_doc_picker)

        ## COSMOS REINDEX BUTTON
        self.gr_cosmos_index_btn = gr.Button(value="🔄 Initiate cosmos refresh (extended journey)", interactive=True, visible=True)
        self.gr_elements.append(self.gr_cosmos_index_btn)

        ## COSMOS RESULT
        self.gr_cosmos_textbox = gr.Textbox(label='💫 Outcome', placeholder="Outcomes shall materialize here", interactive=False, visible=True)
        self.gr_elements.append(self.gr_cosmos_textbox)

        #--------------[CODEX]--------------#

        # CODEX HEADER
        self.gr_codex_media = gr.Markdown(f"""![](https://raw.githubusercontent.com/RoySadaka/ReposMedia/main/venture/app/codex.png)""")
        self.gr_elements.append(self.gr_codex_media)

        # CODEX SEND BUTTON
        self.gr_dispatch_btn = gr.Button(value="📨 Dispatch", interactive=True, visible=True)
        self.gr_elements.append(self.gr_dispatch_btn)


        # CASUAL DETAILS
        self.gr_casual_details = gr.Markdown('')
        self.gr_elements.append(self.gr_casual_details)

        with gr.Blocks(analytics_enabled=False, theme=gr.themes.Glass(), css=".gradio-container {background-color: #F7EDDA} ") as web_page:
            self.gr_explore_tab.render()
            with self.gr_explore_tab:
                self.gr_explore_media.render()
                self.gr_query_text.render()
                self.gr_doc_picker.render()
                self.gr_call_llm_btn.render()
                self.gr_call_llm_btn.click(self.call_llm_handler, inputs=[self.gr_query_text,self.gr_doc_picker], outputs=self.gr_elements)
                self.gr_venture_response.render()

            self.gr_cosmos_tab.render()
            with self.gr_cosmos_tab:
                self.gr_cosmos_media.render()
                self.gr_file_upload.render()
                self.gr_delete_doc_picker.render()
                self.gr_cosmos_index_btn.render()
                self.gr_cosmos_index_btn.click(self.cosmos_index_handler, inputs=[self.gr_file_upload, self.gr_delete_doc_picker], outputs=self.gr_elements)
                self.gr_cosmos_textbox.render()

            self.gr_interlink_tab.render()
            with self.gr_interlink_tab:
                self.gr_interlink_media.render()
                self.gr_interlink_textbox.render()
                self.gr_captain_details_textbox.render()
                self.gr_dispatch_btn.render()
                self.gr_dispatch_btn.click(self.dispatch_handler, inputs=[self.gr_interlink_textbox], outputs=self.gr_elements)

            self.gr_codex_tab.render()
            with self.gr_codex_tab:
                self.gr_codex_media.render()

            self.gr_casual_details.render()

        web_page.launch(share=self.share, show_api=False)



