from dotenv import load_dotenv
import os
import google.generativeai as genai
from prompts import CROSS_REFERENCING_PROMPT, EXTRACT_SUBGRAPH_PROMPT

load_dotenv()

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(prompt):
    """Generate a response from the LLM model."""
    try:
        # Generate response from LLM
        response = model.generate_content(prompt)
        response_text = response.text

        return response_text
    except Exception as e:
        print(f"Error during LLM processing: {e}")
        return {"error": str(e)}
    
# Example usage

text_1 = """

wikileaks_parsed
100%
B2

Pristina Airport – Possible administrative irregularity regarding tender procedures involving Vendor 1 and Vendor 2

Allegation

Two companies with the same owner took part at least three times in the same Airport tenders.

Background Information

The Kosovo citizen, Vendor 1 and Vendor 2 Representative, is the owner and Director of the Pristina-based Vendor 1 and also a 51% shareholder of the Pristina-Ljubljana-based company Vendor 2. Both companies have their residences at the same address in Pristina.

Both Vendor 1 and Vendor 2 submitted three times in 2003 for the same tenders:

Supply and Mounting of Sonic System in the Fire Station Building. Winner was Vendor 2 with €1,530 followed by Vendor 1 with €1,620. The third company, Vendor 3, did not provide a price offer.

Cabling of Flat Display Information System (FIDS). Winner was Vendor 1 with €15,919 followed by Vendor 2 with €19,248.70. The other two competitors, Vendor 3 and Vendor 4, offered prices of Euro 19,702 and Euro 21,045.

Purchase and fixing of Cramer Antenna. Winner was again Vendor 1 with €3,627.99 followed by Vendor 2 with €3,921. The other two competitors, Vendor 3 and Vendor 4, offered prices of €4,278 and €4,670.
 
 
 	
Pristina Airport – Possible administrative irregularity regarding tender procedures involving Vendor 1 and Vendor 2

Allegation

Two companies with the same owner took part at least three times in the same Airport tenders.

Background Information

The Kosovo citizen, Vendor 1 and Vendor 2 Representative, is the owner and Director of the Pristina-based Vendor 1 and also a 51% shareholder of the Pristina-Ljubljana-based company Vendor 2. Both companies have their residences at the same address in Pristina.

Both Vendor 1 and Vendor 2 submitted three times in 2003 for the same tenders:

Supply and Mounting of Sonic System in the Fire Station Building. Winner was Vendor 2 with €1,530 followed by Vendor 1 with €1,620. The third company, Vendor 3, did not provide a price offer.

Cabling of Flat Display Information System (FIDS). Winner was Vendor 1 with €15,919 followed by Vendor 2 with €19,248.70. The other two competitors, Vendor 3 and Vendor 4, offered prices of Euro 19,702 and Euro 21,045.

Purchase and fixing of Cramer Antenna. Winner was again Vendor 1 with €3,627.99 followed by Vendor 2 with €3,921. The other two competitors, Vendor 3 and Vendor 4, offered prices of €4,278 and €4,670.
Turn on screen reader support
To enable screen reader support, press Ctrl+Alt+Z To learn about keyboard shortcuts, press Ctrl+slash

Welcome to Office editing
Now you can use Docs, Sheets and Slides to edit and share your Office-formatted files
4 collaborators have joined the document.
"""

text_2 = """

wikileaks_parsed
100%
B3

Investigative details

In his/her interviews conducted on 31st August and 14th September 2004, Vendor 1 and Vendor 2 Representative admitted that the fact that both Vendor 1 and Vendor 2 took part together in three Airport tenders put other competitors at a disadvantage, but alleged both companies have never exchanged information with regard to the price offers.

There were doubts whether both companies Vendor 3 and Vendor 4 exist and submitted bids for the three tenders. The ITF investigation, with support from the Kosovo Organised Crime Bureau (KOCB), has found no reference with regard to the existence of the alleged competitor Vendor 4 in Pristina. The alleged company Vendor 3 was found to be a supermarket located in Prizren.

The above-mentioned facts are already part of the ITF case no. 286/04 that was submitted to the International Prosecutor, UNMIK Department of Justice, in October 2004. On 1 December 2004, the ITF contacted the International Prosecutor for a legal assessment of this case. Although this case would clearly be a breach of Economic Law, there is no applicable law in Kosovo for the time being.
 
 
 	
Investigative details

In his/her interviews conducted on 31st August and 14th September 2004, Vendor 1 and Vendor 2 Representative admitted that the fact that both Vendor 1 and Vendor 2 took part together in three Airport tenders put other competitors at a disadvantage, but alleged both companies have never exchanged information with regard to the price offers.

There were doubts whether both companies Vendor 3 and Vendor 4 exist and submitted bids for the three tenders. The ITF investigation, with support from the Kosovo Organised Crime Bureau (KOCB), has found no reference with regard to the existence of the alleged competitor Vendor 4 in Pristina. The alleged company Vendor 3 was found to be a supermarket located in Prizren.

The above-mentioned facts are already part of the ITF case no. 286/04 that was submitted to the International Prosecutor, UNMIK Department of Justice, in October 2004. On 1 December 2004, the ITF contacted the International Prosecutor for a legal assessment of this case. Although this case would clearly be a breach of Economic Law, there is no applicable law in Kosovo for the time being.
Turn on screen reader support
To enable screen reader support, press Ctrl+Alt+Z To learn about keyboard shortcuts, press Ctrl+slash4 collaborators have joined the document.
"""

print(generate_response(EXTRACT_SUBGRAPH_PROMPT + "\n" + text_1))
print(generate_response(CROSS_REFERENCING_PROMPT + "text_1: " + text_1 + "text_2: " + text_2))