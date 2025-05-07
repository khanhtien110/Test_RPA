from playwright.async_api import async_playwright
import re
import json
from datetime import timedelta
import sys
import asyncio

async def wait_and_handle_popup(page, timeout: int = 10) -> str:
    try:
        await page.wait_for_selector('.w2window.w2window_restored.w2popup_window', 
                                   state='visible', 
                                   timeout=timeout * 1000)
        popup_element = await page.locator('.w2window.w2window_restored.w2popup_window').get_attribute('id')
        match = re.search(r'popup(\d+)', popup_element)
        return match.group(1) if match else None
    except Exception:
        return None

async def main(data):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path="C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            headless=False
        )
        
        page = await browser.new_page()
        # await page.set_viewport_size({"width": 1600, "height": 900})
        await page.goto(data["INFO"]["url_A"])
        
        # Wait for network to be idle
        await page.wait_for_load_state('networkidle', timeout=10000)
        
        # Page 1
        await page.click('#mf_wfm_potal_main_img_mymenu_0')
        await page.wait_for_selector('#mf_wfm_potal_main_wfm_content_sbx_smpl_swrd___input', state='visible')
        await page.wait_for_load_state('networkidle', timeout=30000)
        await page.fill('#mf_wfm_potal_main_wfm_content_sbx_smpl_swrd___input', 
                        data["OptionA"]["Address"], 
                        force=True)
        
        await page.click('#mf_wfm_potal_main_wfm_content_btn_smpl_srch')
        
        # Page 2
        await page.click('#mf_wfm_potal_main_wfm_content_grd_smpl_srch_rslt_chk_all label')
        await page.click('#mf_wfm_potal_main_wfm_content_btn_next')
        
        await page.click('#mf_wfm_potal_main_wfm_content_grd_loc_srch_rslt_chk_all label')
        await page.click('#mf_wfm_potal_main_wfm_content_btn_next')
        
        # Page 3
        await page.click('#mf_wfm_potal_main_wfm_content_chk_rgs_mttr_cls li:nth-child(1)')
        await page.click('#mf_wfm_potal_main_wfm_content_chk_rgs_mttr_cls li:nth-child(2)')
        await page.click('#mf_wfm_potal_main_wfm_content_btn_next')
        
        await page.click('#mf_wfm_potal_main_wfm_content_grd_cmort_list_cmort_chk_all label')
        await page.click('#mf_wfm_potal_main_wfm_content_btn_next')
        
        # Page 4
        await page.click('#mf_wfm_potal_main_wfm_content_btn_bpay')
        
        popup_id = await wait_and_handle_popup(page)
        if popup_id:
            await page.fill(f'#mf_wfm_potal_main_wfm_content_popup{popup_id}_wframe_popup_user_id_g___input', 
                           data["INFO"]["LoginPW"], 
                           force=True)
            await page.fill(f'#mf_wfm_potal_main_wfm_content_popup{popup_id}_wframe_popup_mbr_pw_g', 
                           data["INFO"]["LoginPW"], 
                           force=True)
            await page.click(f'#mf_wfm_potal_main_wfm_content_popup{popup_id}_wframe_btn_popup_login_g')
        
        await page.wait_for_load_state('networkidle', timeout=30000)
        popup_id_payment = await wait_and_handle_popup(page, timeout=2)
        
        if popup_id_payment:
            await page.click(f'#mf_wfm_potal_main_wfm_content_popup{popup_id_payment}_wframe_btn_bpay')
        else:
            await browser.close()
            return
        
        # Page 5
        await page.wait_for_selector('#mf_wfm_potal_main_wfm_content_tac_bpay_mthd_tab_tab_pp_tabHTML', 
                                    state='visible', 
                                    timeout=30000)
        await page.evaluate('document.getElementById("mf_wfm_potal_main_wfm_content_tac_bpay_mthd_tab_tab_pp_tabHTML").click();')
        
        await page.type('#mf_wfm_potal_main_wfm_content_sbx_emoney_code1___input', 
                        data["INFO"]["PayNumber1"], 
                        delay=100)
        await page.type('#mf_wfm_potal_main_wfm_content_sbx_emoney_code2___input', 
                        data["INFO"]["PayNumber2"], 
                        delay=100)
        await page.type('#mf_wfm_potal_main_wfm_content_sct_emoney_pwd', 
                        data["INFO"]["PayNumber3"], 
                        delay=100)
        
        await page.click('#mf_wfm_potal_main_wfm_content_chk_whl_agree li:first-child')
        await page.evaluate('document.getElementById("mf_wfm_potal_main_wfm_content_btn_bpay").click();')
        
        # Payment Error
        popup_id_payment_error = await wait_and_handle_popup(page, timeout=2)
        if popup_id_payment_error:
            await page.click(f'#mf_wfm_potal_main_wfm_content_popup{popup_id_payment_error}_wframe_btn_confirm')
            await browser.close()
            sys.exit(0)
        else:
            await browser.close()
            return
