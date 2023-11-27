import scrapy
from ..cleaning import clean


class CrunchbasespiderSpider(scrapy.Spider):
    name = 'CrunchBaseSpider'
    
    BASE_URL = "https://www.crunchbase.com"
    start_urls = ['https://www.crunchbase.com/organization/ecovative-designs']

    def parse(self, response):
        item = {}
        item['Comapny_Url'] = response.url
        item['Address'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[1]//li)[1])').get()
        item['Number_Of_Employess'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[1]//li)[2])').get()
        item['Company_Website'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[1]//li)[5])').get()
        item['Company_Type'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[1]//li)[4])').get()
        item['Industries'] = response.xpath('(//section-card[@class="ng-star-inserted"])[4]//li//div[@class="cb-overflow-ellipsis"]/text()').getall()
        item['Headquarters_Regions'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[2]//field-formatter)').get()
        item['Founded_Date'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[3]//field-formatter)').get()
        item['Founders'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[4]//field-formatter)').get()
        item['Operating_Status'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[5]//field-formatter)').get()
        item['Last_Funding_Type'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[6]//field-formatter)').get()
        item['Legal_Name'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[7]//field-formatter)').get()
        # item['Company_Type'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[8]//field-formatter)').get()
        item['Contact_Email'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[9]//field-formatter)').get()
        item['Phone_Number'] = response.xpath('normalize-space(((//section-card[@class="ng-star-inserted"])[4]//li)[10]//field-formatter)').get()
        item['Description'] = response.xpath('normalize-space((//section-card[@class="ng-star-inserted"])[4]//description-card)').get()
        
        next_url = "https://www.crunchbase.com/organization/ecovative-designs/company_financials"
        yield scrapy.Request(url=next_url, callback=self.parse_financial, meta={'item' : item})


    def parse_financial(self, response):
        above__meta_data_1 =  response.meta.get("item")
        item = {}
        item['Financial_Url'] = response.url
        item['Lead_Investment'] = self.parse_lead_investments(response)
        item['Investments'] = self.parse_investments(response)
        item['Funding_Round'] = self.parse_funding_round(response)
        item['Total_Funding_Amount'] = response.xpath('normalize-space((//profile-section//anchored-values/div)[4]//field-formatter)').get()
        item['Lead_Investors'] = response.xpath('normalize-space((//profile-section//anchored-values/div)[5]//field-formatter)').get()
        item['Investors'] = response.xpath("normalize-space((//profile-section//anchored-values/div)[6]//field-formatter)").get()
        item['Funding_Rounds_Details'] = self.parse_funding_round_details(response)
        item['Investors_Detail'] = self.parse_investors_details(response)
        
        next_url = "https://www.crunchbase.com/organization/ecovative-designs/org_similarity_overview"
        yield scrapy.Request(url=next_url, callback=self.parse_similar_companies, meta = {"item1": above__meta_data_1, "item2" : item})
    
    
    def parse_similar_companies(self, response):
        
        item = {}
        item['Comapny_Url'] = response.meta.get("item1")['Comapny_Url']
        item['Address'] = response.meta.get("item1")['Address']
        item['Number_Of_Employess'] = response.meta.get("item1")['Number_Of_Employess']
        item['Company_Website'] = response.meta.get("item1")['Company_Website']
        item['Company_Type'] = response.meta.get("item1")['Company_Type']
        item['Industries'] = response.meta.get("item1")['Industries']
        item['Headquarters_Regions'] = response.meta.get("item1")['Headquarters_Regions']
        item['Founded_Date'] = response.meta.get("item1")['Founded_Date']
        item['Founders'] = response.meta.get("item1")['Founders']
        item['Operating_Status'] = response.meta.get("item1")['Operating_Status']
        item['Last_Funding_Type'] = response.meta.get("item1")['Last_Funding_Type']
        item['Legal_Name'] = response.meta.get("item1")['Legal_Name']
        item['Contact_Email'] = response.meta.get("item1")['Contact_Email']
        item['Phone_Number'] = response.meta.get("item1")['Phone_Number']
        item['Description'] = response.meta.get("item1")['Description']
        item['Financial_Url'] = response.meta.get("item2")['Financial_Url']
        item['Lead_Investment'] = response.meta.get("item2")['Lead_Investment']
        item['Investments'] = response.meta.get("item2")['Investments']
        item['Funding_Round'] = response.meta.get("item2")['Funding_Round']
        item['Total_Funding_Amount'] = response.meta.get("item2")['Total_Funding_Amount']
        item['Lead_Investors'] = response.meta.get("item2")['Lead_Investors']
        item['Investors'] = response.meta.get("item2")['Investors']
        item['Funding_Rounds_Details'] = response.meta.get("item2")['Funding_Rounds_Details']
        item['Investors_Detail'] = response.meta.get("item2")['Investors_Detail']
        item['Similar_Companies_Page_Url'] = response.url
        item['Similar_Companies'] = self.parse_similar_comp(response)
        yield  item   
    
    
    def parse_similar_comp(self, response):
        companies = response.xpath("//org-similarity-card/div//org-similarity-card-item")
        data = []
        for company in companies:
            dict_item = {}
            dict_item['Company_Name'] = company.xpath("normalize-space((.//identifier-link)[1])").get()
            try:
                dict_item['Company_Url'] = self.BASE_URL + company.xpath("normalize-space((.//identifier-link/a/@href)[1])").get()
            except:
                dict_item['Company_Url'] = ""
            data.append(dict_item)
        return data
    
    
    def parse_lead_investments(self, response):
        Lead_Investment = response.xpath('normalize-space((//profile-section//anchored-values/div)[1]//field-formatter)').get()
        return Lead_Investment

    def parse_investments(self, response):
        Investments = response.xpath('normalize-space((//profile-section//anchored-values/div)[2]//field-formatter)').get()
        return Investments
    
    def parse_funding_round(self, response):
        Funding_Round = response.xpath('normalize-space((//profile-section//anchored-values/div)[3]//field-formatter)').get()
        return Funding_Round
    
    def parse_funding_round_details(self, response):
        rows = response.xpath("(//profile-section)[3]//list-card//table//tbody/tr")
        data = []
        for i in rows:
            dict_item = {}
            dict_item['Announced_Date'] = i.xpath("normalize-space((.//td//field-formatter)[1])").get()
            dict_item['Transaction_Name'] = i.xpath("normalize-space((.//td//field-formatter)[2])").get()
            try:
                dict_item['Transaction_Url'] = self.BASE_URL + i.xpath("(.//td)[2]//a/@href").get()
            except:
                dict_item['Transaction_Url'] = ""
            dict_item['Number_Of_Investors'] = i.xpath("normalize-space((.//td//field-formatter)[3])").get()
            try:
                dict_item['Number_Of_Investors_Url'] = self.BASE_URL + i.xpath("(.//td)[3]//a/@href").get()
            except:
                dict_item['Number_Of_Investors_Url'] = ""
            dict_item['Money_Raised'] = clean(i.xpath("normalize-space((.//td//field-formatter)[4])").get())
            dict_item['Lead_Investors'] = clean(i.xpath("normalize-space((.//td//field-formatter)[5])").get())
            try:
                dict_item['Lead_Investors_Url'] = self.BASE_URL + i.xpath("(.//td)[5]//a/@href").get()
            except:
                dict_item['Lead_Investors_Url'] = ""
            data.append(dict_item)
        return data
    
    def parse_investors_details(self, response):
        rows = response.xpath("(//profile-section)[4]//list-card//table//tbody/tr")
        data = []
        for i in rows:
            dict_item = {}
            dict_item['Investor_Name'] = i.xpath("normalize-space((.//td//field-formatter)[1])").get()
            try:
                dict_item['Investor_Name_Url'] = self.BASE_URL + i.xpath("(.//td)[1]//a/@href").get()
            except:
                dict_item['Investor_Name_Url'] = ""
            dict_item['Lead_Investor'] = clean(i.xpath("normalize-space((.//td//field-formatter)[2])").get())
            dict_item['Funding_Round'] = clean(i.xpath("normalize-space((.//td//field-formatter)[3])").get())
            try:
                dict_item['Funding_Round_Url'] = self.BASE_URL + i.xpath("(.//td)[3]//a/@href").get()
            except:
                dict_item['Funding_Round_Url'] = ""
            dict_item['Partners'] = clean(i.xpath("normalize-space((.//td//field-formatter)[4])").get())
            try:
                dict_item['Partners_Url'] = self.BASE_URL + i.xpath("(.//td)[4]//a/@href").get()
            except:
                dict_item['Partners_Url'] = ""
            data.append(dict_item)
        return data