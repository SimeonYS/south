import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SouthItem
from itemloaders.processors import TakeFirst
import requests
import json
from scrapy import Selector

pattern = r'(\xa0)?'

url = "https://southernstatesbank.net/category/news/"

payload = "pp_action=get_ajax_posts&node_id=5d7ba145ce398&paged={}&current_page=https%3A%2F%2Fsouthernstatesbank.net%2Fcategory%2Fnews%2F&settings%5Blayout%5D=grid&settings%5Bpost_grid_style_select%5D=style-6&settings%5Balternate_content%5D=no&settings%5Bcustom_layout%5D%5Bhtml%5D=%5Bwpbb-if+post%3Afeatured_image%5D%0A%3Cdiv+class%3D%22pp-content-grid-post-image%22%3E%0A%09%5Bwpbb+post%3Afeatured_image+size%3D%22large%22+display%3D%22tag%22+linked%3D%22yes%22%5D%0A%3C%2Fdiv%3E%0A%5B%2Fwpbb-if%5D%0A%0A%3Cdiv+class%3D%22pp-content-grid-post-text%22%3E%0A%0A++++%3Ch3+class%3D%22pp-content-grid-post-title%22%3E%5Bwpbb+post%3Alink+text%3D%22title%22%5D%3C%2Fh3%3E%0A%0A++++%3Cdiv+class%3D%22pp-content-grid-post-meta%22%3E%0A++++%09%5Bwpbb+post%3Adate+format%3D%22F+j%2C+Y%22%5D%0A%09%09%3Cspan+class%3D%22pp-content-grid-post-meta-sep%22%3E+%7C+%3C%2Fspan%3E%0A%09%09%5Bwpbb+post%3Aterms_list+taxonomy%3D%22category%22+separator%3D%22%2C+%22%5D%0A++++%3C%2Fdiv%3E%0A%0A%09%3Cdiv+class%3D%22pp-content-grid-separator%22%3E%3C%2Fdiv%3E%0A%0A++++%3Cdiv+class%3D%22pp-content-grid-post-excerpt%22%3E%0A++++%09%5Bwpbb+post%3Aexcerpt+length%3D%2217%22+more%3D%22...%22%5D%0A++++%3C%2Fdiv%3E%0A%0A++++%3Cdiv+class%3D%22pp-content-grid-post-more-link%22%3E%0A++++%09%3Ca+href%3D%22%5Bwpbb+post%3Aurl%5D%22%3E%3Cspan+class%3D%22fa+fa-angle-right%22%3E%3C%2Fspan%3E+Read+More%3C%2Fa%3E%0A++++%3C%2Fdiv%3E%0A%0A%3C%2Fdiv%3E%0A&settings%5Bcustom_layout%5D%5Bcss%5D=.pp-content-grid-post+%7B%0A++++font-size%3A+14px%3B%0A%7D%0A.pp-content-grid-post-image+%7B%0A++++padding%3A+20px%3B%0A++++padding-bottom%3A+0%3B%0A%7D%0A.pp-content-grid-post-text+%7B%0A++++padding%3A+20px%3B%0A%7D%0A.pp-content-grid-post-title+%7B%0A++++font-size%3A+20px%3B%0A%09line-height%3A+26px%3B%0A%09margin%3A+0%3B%0A%09padding%3A+0%3B%0A%7D%0A.pp-content-grid-post-meta+%7B%0A++++padding%3A+0%3B%0A%7D%0A.pp-content-grid-post-meta+a+%7B%0A++++text-decoration%3A+none%3B%0A%7D%0A.pp-content-grid-post-meta%2C%0A.pp-content-grid-post-meta+a+%7B%0A++++color%3A+%23888%3B%0A++++font-size%3A+12px%3B%0A%7D%0A.pp-content-grid-post-meta+a%3Ahover+%7B%0A++++color%3A+%23000%3B%0A%7D%0A.pp-content-grid-separator+%7B%0A++++min-height%3A+2px%3B%0A++++width%3A+60px%3B%0A++++background%3A+%23000%3B%0A++++margin-top%3A+10px%3B%0A++++margin-bottom%3A+20px%3B%0A%7D%0A&settings%5Btotal_post%5D=all&settings%5Btotal_posts_count%5D=20&settings%5Bposts_per_page%5D=6&settings%5Bexclude_current_post%5D=no&settings%5Bpagination%5D=scroll&settings%5Bload_more_text%5D=Load+More&settings%5Bno_results_message%5D=Sorry%2C+we+couldn't+find+any+posts.+Please+try+a+different+search.&settings%5Bshow_search%5D=yes&settings%5Bpagination_nofollow%5D=no&settings%5Btitle_tag%5D=h3&settings%5Bvisibility_logic%5D=%5B%5D&settings%5Bzindex%5D=&settings%5Bexport%5D=&settings%5Bimport%5D=&settings%5Btype%5D=pp-content-grid&settings%5Bpost_border_width%5D=1&settings%5Bfield_separator_0%5D=&settings%5Bdata_source%5D=custom_query&settings%5Bpost_type%5D=post&settings%5Border_by%5D=date&settings%5Border_by_meta_key%5D=&settings%5Border%5D=DESC&settings%5Boffset%5D=0&settings%5Bposts_post_matching%5D=1&settings%5Bposts_post%5D=&settings%5Btax_post_category_matching%5D=1&settings%5Btax_post_category%5D=&settings%5Btax_post_post_tag_matching%5D=1&settings%5Btax_post_post_tag%5D=&settings%5Bposts_page_matching%5D=1&settings%5Bposts_page%5D=&settings%5Bposts_download_matching%5D=1&settings%5Bposts_download%5D=&settings%5Btax_download_download_category_matching%5D=1&settings%5Btax_download_download_category%5D=&settings%5Btax_download_download_tag_matching%5D=1&settings%5Btax_download_download_tag%5D=&settings%5Busers_matching%5D=1&settings%5Busers%5D=&settings%5Bshow_content%5D=no&settings%5Bcontent_type%5D=content&settings%5Bcontent_length%5D=20&settings%5Bmore_link_type%5D=button&settings%5Bmore_link_text%5D=Read+More&settings%5Bpost_grid_filters_display%5D=no&settings%5Bpost_grid_filters%5D=post_tag&settings%5Bproduct_rating%5D=yes&settings%5Bproduct_price%5D=yes&settings%5Bproduct_button%5D=yes&settings%5Bshow_image%5D=yes&settings%5Bimage_thumb_size%5D=full&settings%5Bimage_thumb_crop%5D=&settings%5Bshow_author%5D=no&settings%5Bshow_date%5D=yes&settings%5Bshow_categories%5D=no&settings%5Bpost_taxonomies%5D=category&settings%5Bmeta_separator%5D=+%7C+&settings%5Bconnections%5D%5Barrow_color%5D=&settings%5Bconnections%5D%5Barrow_hover_color%5D=&settings%5Bconnections%5D%5Barrow_bg_color%5D=&settings%5Bconnections%5D%5Barrow_bg_hover_color%5D=&settings%5Bconnections%5D%5Barrow_border_hover_color%5D=&settings%5Bconnections%5D%5Bpost_slider_dot_bg_color%5D=&settings%5Bconnections%5D%5Bpost_slider_dot_bg_hover%5D=&settings%5Bconnections%5D%5Bcustom_content%5D=&settings%5Bconnections%5D%5Bmore_link_text%5D=&settings%5Bconnections%5D%5Ball_filter_label%5D=&settings%5Bconnections%5D%5Bpost_bg_color%5D=&settings%5Bconnections%5D%5Bpost_bg_color_hover%5D=&settings%5Bconnections%5D%5Bpost_title_divider_color%5D=&settings%5Bconnections%5D%5Bpost_category_bg_color%5D=&settings%5Bconnections%5D%5Bpost_category_text_color%5D=&settings%5Bconnections%5D%5Bpost_title_overlay_color%5D=&settings%5Bconnections%5D%5Bpost_date_day_bg_color%5D=&settings%5Bconnections%5D%5Bpost_date_day_text_color%5D=&settings%5Bconnections%5D%5Bpost_date_month_bg_color%5D=&settings%5Bconnections%5D%5Bpost_date_month_text_color%5D=&settings%5Bconnections%5D%5Bpost_date_bg_color%5D=&settings%5Bconnections%5D%5Bpost_date_text_color%5D=&settings%5Bconnections%5D%5Bproduct_rating_color%5D=&settings%5Bconnections%5D%5Bproduct_price_color%5D=&settings%5Bconnections%5D%5Bbutton_bg_color%5D=&settings%5Bconnections%5D%5Bbutton_bg_hover_color%5D=&settings%5Bconnections%5D%5Bbutton_text_color%5D=&settings%5Bconnections%5D%5Bbutton_text_hover_color%5D=&settings%5Bconnections%5D%5Bbutton_border_hover_color%5D=&settings%5Bconnections%5D%5Bfilter_bg_color%5D=&settings%5Bconnections%5D%5Bfilter_bg_color_active%5D=&settings%5Bconnections%5D%5Bfilter_text_color%5D=&settings%5Bconnections%5D%5Bfilter_text_color_active%5D=&settings%5Bconnections%5D%5Bfilter_border_hover_color%5D=&settings%5Bconnections%5D%5Bfilter_toggle_bg%5D=&settings%5Bconnections%5D%5Bfilter_toggle_color%5D=&settings%5Bconnections%5D%5Bpagination_bg_color%5D=&settings%5Bconnections%5D%5Bpagination_bg_color_hover%5D=&settings%5Bconnections%5D%5Bpagination_color%5D=&settings%5Bconnections%5D%5Bpagination_color_hover%5D=&settings%5Bconnections%5D%5Btitle_font_color%5D=&settings%5Bconnections%5D%5Bcontent_font_color%5D=&settings%5Bconnections%5D%5Bpost_meta_font_color%5D=&settings%5Bconnections%5D%5Bpost_meta_bg_color%5D=&settings%5Bconnections%5D%5Bevent_date_color%5D=&settings%5Bconnections%5D%5Bevent_venue_color%5D=&settings%5Bconnections%5D%5Bevent_cost_color%5D=&settings%5Bdata_source_acf_relational_type%5D=relationship&settings%5Bdata_source_acf_relational_key%5D=&settings%5Bshow_title%5D=yes&settings%5Bcustom_content%5D=&settings%5Bpost_grid_filters_type%5D=dynamic&settings%5Ball_filter_label%5D=All&settings%5Bfallback_image%5D=custom&settings%5Bfallback_image_custom%5D=269&settings%5Bas_values_posts_post%5D=&settings%5Bas_values_tax_post_category%5D=&settings%5Bas_values_tax_post_post_tag%5D=&settings%5Bas_values_posts_page%5D=&settings%5Bas_values_users%5D=&settings%5Bfallback_image_custom_src%5D=https%3A%2F%2Fsouthernstatesbank.net%2Fwp-content%2Fuploads%2F2019%2F10%2Fimage-bank.jpg&is_archive=true&is_tax=true&taxonomy=category&term=news"
headers = {
    'authority': 'southernstatesbank.net',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'accept': '*/*',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://southernstatesbank.net',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://southernstatesbank.net/category/news/',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': '_ga=GA1.2.1644923722.1616578041; _gid=GA1.2.833436193.1616578041'
}


class SouthSpider(scrapy.Spider):
    name = 'south'
    page = 1
    start_urls = ['https://southernstatesbank.net/category/news/']

    def parse(self, response):
        data = requests.request("POST", url, headers=headers, data=payload.format(self.page))
        data = json.loads(data.text)
        container = data['data']
        links = Selector(text=container).xpath('//h3[@class="pp-content-grid-title pp-post-title"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_post)

        if data['pagination']:
            self.page += 1
            yield response.follow(response.url, self.parse, dont_filter=True)

    def parse_post(self, response):
        date = response.xpath('//script[@type="application/ld+json"]/text()').get()
        date = json.loads(date)
        try:
            date_published = date['@graph'][5]['datePublished'].split('T')[0]
        except IndexError:
            date_published = date['@graph'][4]['datePublished'].split('T')[0]
        title = response.xpath('(//h2[@class="fl-heading"]/span)[2]//text()').get()
        content = response.xpath('(//div[@class="fl-row-content-wrap"]//div[@class="fl-col-content fl-node-content"])[5]//text()[not (ancestor::div[@class="wp-block-image"])]').getall()
        content = [p.strip() for p in content if p.strip()]
        content = re.sub(pattern, "",' '.join(content))

        item = ItemLoader(item=SouthItem(), response=response)
        item.default_output_processor = TakeFirst()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        item.add_value('date', date_published)

        yield item.load_item()
