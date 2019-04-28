import arcpy
import os

inputFolder = r'C:\Users\tmoran\Desktop\msga580\final_project\data'
inputArtists = r'C:\Users\tmoran\Desktop\msga580\final_project\data\npr_data.gdb\tiny_desk_locations'
gdbName = 'npr_artists'

def createArtistgdb(folder,gdbName):
	gdb = str(arcpy.CreateFileGDB_management(folder,gdbName, "CURRENT" ))
	return gdb



workspace = createArtistgdb(inputFolder, gdbName)

arcpy.env.overwriteOutput = True

fields = [
    
["artist",'Artist/Group','TEXT', 50, 'artists' ], 
["venue", 'Venue where you saw them', 'TEXT', 50, None],
["rating", 'Rating 0-10', 'SHORT', 2, 'rating'],
]

def createDomainList(inputArtists):
    with arcpy.da.SearchCursor(inputArtists, ['guid_','title']) as cursor:
        for row in cursor:
            try: 
                guid = str(row[0])
                artist = str(row[1])
                artists.append([guid, artist])
            except: 
                guid = row[0]
                artist = row[1]

                print guid
                print artist
    print artists

def createArtistConcertTrackerLayer(workspace,artistLookupTableName):
	artistTable = os.path.join(workspace, artistLookupTableName)
	crs = arcpy.SpatialReference(4326)
	arcpy.CreateFeatureclass_management(workspace, artistLookupTableName, "POINT", spatial_reference= crs)

	return artistTable #return reference to newly created artist Table

def addDomains(workspace,domains):
    for key, values in domains.items():
        val1 = values[0]
        val2 = values[1]
        arcpy.CreateDomain_management(workspace, key,val1,val2)

def addRatings(workspace):
    """add coded domain values to domain"""
    for i in range(1, 11): 
        arcpy.AddCodedValueToDomain_management (workspace, 'rating', i, "Rating: {0}/10".format(str(i)))

def addDomainValues(workspace,domain_values ):
    for key, values in domain_values.items():
        for item in values:
            val1 = item[0]
            val2 =  item[1]
            arcpy.AddCodedValueToDomain_management (workspace,key,val1,val2)

def assignDomainToField(layer, field, domain_name):
    try: 
        arcpy.AssignDomainToField_management (layer, field, domain_name)
    except: 
        print "Issue assigning domain to {0} field".format(field)

def addFields(feature_layer, fields):
    #ADDS INPUT FIELDS ACCORDING TO INPUT FIELDS OBJECT PROVIDED BY FIELDS DICT WHERE KEY: Fieldname, value[0]: Alias Name, value[1]: field type, value[2]:field length
    for field in fields:  
        arcpy.AddField_management(feature_layer, field[0], field_alias= field[1], field_type= field[2], field_length= field[3])
    


artistLookupTableName = "NPR_Artists"
artists = []

domains = {
    "artists": ['Previous NPR Artists', 'TEXT'],
    "rating": ['Artist Rating', 'TEXT']
}

artistDomains = {'artists': [
    ['a65bcf72-de6b-42f7-8d50-0195cc329839', 'Gabriel Garzon-Montano'],
    ['d9790f7b-d85b-4e08-b77c-b019eaa24531', 'Dan Auerbach'], 
    ['fcd1d082-a1f6-42a1-a029-aec96619464a', 'The Shins'], 
    ['12581350-b89a-4d8f-ac59-6824c505dde9', 'Bedouine'], 
    ['30fc6ad3-06fc-404b-a389-638b05f890d8', '&More (Chill Moody & Donn T)'],
    ['d6849b59-0b71-48de-a094-63bcaacc19da', 'Maren Morris'], 
    ['a63b4481-bd7e-40b8-b75a-50824b57231e', 'Drive-By Truckers'],
    ['212e0966-35d9-45f9-a5d7-fd1de5639840', 'Cat Power'],
    ['28d07764-716e-4e5f-ad75-72c18f7d37f8', 'T.I.'],
    ['4b9f810e-c368-44f2-8f3b-2b68510d59f1', 'Royal Thunder'], 
    ['60a74c0a-716f-405e-a1ec-073dd2d9f890', 'Aldous Harding'],
    ['897052ef-6b47-4a0a-b16c-8c3064668c13', 'Gary Clark Jr.'],
    ['3f8b8a6f-5ef5-4683-99af-f272565f63e1', 'Snail Mail'],
    ['41c36949-dc40-49dc-941d-feec142abc93', 'Amadou and Mariam'],
    ['4ed17565-f6a1-40a0-9c4e-15308cf6e513', 'Bleachers'],
    ['3678f08c-d7b6-4ccb-a2b5-fc59397b90dd', 'Gucci Mane'],
    ['cb8d3716-0d04-4c44-9f0e-aca9deda9a79', 'Bomba Estereo'],
    ['bb6e85d4-5260-4b0e-b632-51036074c051', 'The Breeders'],
    ['0e4092d9-0644-457a-bfab-8c4656feb698', 'The Perceptionists'],
    ['714d90ef-ec98-43ed-84b7-1007b0ca86de', 'AHI'], 
    ['54cd841d-bac5-4222-9134-d9b6bfeb7069', 'Liniker e os Caramelows'],
    ['61b80ea4-63ff-473f-afb4-192fef7d0545', 'Dirty Projectors'],
    ['0a987cca-727a-4ebb-9ce5-1d64a80c5fe0', 'GZA & The Soul Rebels'], 
    ['db710313-a797-4386-9780-1cfc26516e20', 'O.C.'], 
    ['3d0f30f9-7885-447b-8152-0c866aa0ecde', 'Big Daddy Kane'], 
    ['210cce63-1c3a-4fae-8989-51dd4528d799', 'Big Thief'],
    ['20c5b9d9-61d9-424a-851c-ffd7deaece67', 'Julie Byrne'],
    ['f3f318c2-eee3-4352-afa0-f87395edc870', 'Ani DiFranco'],
    ['ad50a5fe-9985-4cf4-9c63-9703bebfb983', 'Tegan And Sara'], 
    ['592e2c47-66ba-4460-a57d-1057a4eed6b4', "The King's Singers"],
    ['0f126642-cd46-4062-b068-6b86f59203cd', 'Lalah Hathaway'],
    ['265cb4a5-4bb8-436f-bf0a-3b7843855cb3', 'Third Coast Percussion'],
    ['2f2e075d-4034-40e2-9672-0c15aea9a7a7', 'Open Mike Eagle'],
    ['2bacb96e-4e97-491d-bffc-9f161b7ebee2', 'Rachel Barton Pine'],
    ['7cd7ebc8-d794-4fb7-acd2-8fbea8ca0562', 'Cafe Tacvba'],
    ['af5f6aec-e2cf-46d2-a7a6-be8993847c60', 'Natalia Lafourcade'],
    ['0a8c36ce-5e2c-4ee9-8b8d-e279e67085d8', 'The Calidore String Quartet'],
    ['bd897350-d6ab-43a1-9726-84131f525ee6', 'Theodore'],
    ['2bb3450f-675d-4d56-b920-e3422030c773', 'Karine Polwart Trio'],
    ['d1482662-ea89-427a-b4cc-e1b97f5e64f1', 'Andrea Cruz'],
    ['28339f42-dbd6-4b18-b9d8-a00bc68904a2', 'Nao'],
    ['97c7681d-561c-4c88-9a53-576cfccb3dcb', 'Leikeli47'],
    ['1a725ea8-66d1-4767-8239-60610e525acd', 'Meg Myers'], 
    ['8a744987-ab50-4142-80ea-06b81b25eaad', 'Phony Ppl'], 
    ['0ba774d7-664d-443e-bb6c-868ae8151e16', 'Zaytoven'], 
    ['0bf4990d-69c7-4889-b60c-07913f213ee1', 'Natalie Prass'],
    ['ec95a449-869d-4adf-b8fa-cf2913ca26c7', 'The Pedrito Martinez Group'],
    ['a4d9e33c-7c36-45aa-9104-5d14cb43090f', 'Scott Mulvahill'],
    ['14a177d2-b454-4c95-82c7-aeb65329f7da', 'Mountain Man'], 
    ['05e9360d-fdd7-417c-8d7e-81b5d1457cdb', 'Lau Noah'], 
    ['88d28d9e-95c4-4e0f-8226-4c822aa1f38d', 'Nate Wood - fOUR'],
    ['22a96283-8692-44c4-b1c6-918bd737892a', 'Aaron Lee Tasjan'],
    ['dd89c988-993b-429c-b5be-2238eceff35b', 'Carolina Eyck and Clarice Jensen'],
    ['220e98ce-22d1-438a-b622-59a65c68824b', 'Miguel Zenan feat. Spektral Quartet'], 
    ['a74988c1-5446-4819-a9e1-ecdb482af45d', 'Harold Lopez-Nussa Trio'], 
    ['88a8a3d2-57d5-4cb1-ad5d-c29365640a05', 'Amy Grant'], 
    ['5e55375c-00b5-40b1-99a2-41df124e0d2e', 'H.E.R.'],
    ['fc07e198-97f5-4bb8-9c99-9bd1119a960c', 'Joey Alexander'],
    ['21f6ac4a-daa0-4a6f-bf1b-7ffd5f2cf2fd', 'The Innocence Mission'],
    ['48b4a978-a381-46bc-967c-a45e07c75349', 'dvsn'],
    ['2ed4386d-960b-4ddc-bc42-0658aaefd2f1', 'boygenius'],
    ['db49b3d5-4516-4c25-8a5c-4a07424c84a9', 'Bernie And The Believers Feat. Essence: Tiny Desk Concert'],
    ['d5ec96f2-8d14-4127-860e-a2d0cabbc7c5', 'Half Waif'],
    ['4354fc9d-d72d-465d-bfe9-ed2eb9bc2627', 'Nicholas Payton Trio'], 
    ['f6703c95-2be8-4fbe-8841-ec049c5cc5fd', 'Cautious Clay'],
    ['8f6da810-76c8-4f8c-bfed-487122bb4f2a', 'Florence + the Machine'], 
    ['1a96a34b-4215-4652-ae52-278c48a42014', 'Cory Henry'], 
    ['32c2d595-3f1f-4c0b-a77d-7d8f0171b86b', 'Saba'],
    ['bdf2ce06-f368-43eb-960e-17b477a4930b', 'Smif-N-Wessun'],
    ['a3109fd3-957d-4a36-87ac-06de3b93319d', 'GoGo Penguin'],
    ['2c13e058-2bba-4fdc-b690-abe2f4c82ece', 'Hobo Johnson and The Lovemakers'],
    ['3dd91e18-5333-4930-9b9a-e162bf549d3d', 'Jupiter & Okwess'], 
    ['8fae4db8-a7ba-440b-b83e-f0dc8f415941', 'Kalbells'],
    ['37c987a7-d6d3-41e4-968c-2e3561962877', 'George Li'],
    ['47587e49-b3ec-41e4-829e-8aa61dfd0456', 'Tech N9ne Feat. Krizz Kaliko: Tiny Desk Concert'],
    ['152a8702-de04-4eee-a1a9-ae629055503c', 'Dermot Kennedy'], 
    ['5b761dfc-40bd-47e8-b361-6ccc73220121', 'Flasher'], 
    ['9b2bbcfd-cc9d-4375-b3c0-dc24fc9c2ef1', 'The Midnight Hour'],
    ['65df9a49-c28e-4e16-9cad-c1fba6506cbd', 'Mumu Fresh Feat. Black Thought & DJ Dummy'],
    ['bd3637b1-411e-4734-b2f5-e1a6d312a01f', 'Rev. Sekou And The Seal Breakers'], 
    ['8f59197e-c53a-4e0c-a451-a18ad55f5d83', 'Frederic Yonnet With Special Guest Dave Chappelle']
    , ['51ece4cc-5400-4c7e-925e-f18f86ba53b9', 'PJ Morton'],
    ['ff7b6f39-b09c-46bc-9f25-03a9e1c4d78b', 'Golden Dawn Arkestra'], 
    ['9a54d5d4-36b9-4dbb-9612-8fdebde3f641', 'Dave Matthews'], 
    ['0a2bdcd3-5959-4b92-86da-9234843249c3', 'From The Top'],
    ['3355c7ba-c2d7-4e68-9b6a-d6cc691ad4a4', 'The Messthetics'], 
    ['516564ae-da51-41b7-be8d-c381944bdf69', 'Yissy Garcia & Bandancha'],
    ['0b507f92-454e-47ce-9dcf-5f8a1defbd02', 'MILCK'], 
    ['6f9e10f7-5670-49d3-957b-2691f761b21b', 'Tom Misch'], 
    ['53e4ffdb-0353-4868-8255-7522c0ebc69d', 'Ill Camille'], 
    ['bf17a10d-4d24-4919-95d7-162152d9a161', "The Band's Visit"], 
    ['34d6afef-8066-40f8-ad0d-d03de8777d58', 'Partner'],
    ['b3a99a69-c253-4b43-a4d4-0def5b35dfba', 'Khruangbin'], 
    ['d2cd0c6c-1145-42df-b979-4c1d20dd2afc', 'Naia Izumi'],
    ['b7d59fd2-c16d-4931-a4b2-dc05e63dc2d0', 'Bela Fleck and Abigail Washburn'],
    ['f048508e-0c96-4183-9e5b-0f34f1bb1fed', 'Gordi'],
    ['a8d61cf7-2596-48ea-b73d-e938518f5dbc', 'Darlingside'], 
    ['c544bd0f-0f75-490d-9e25-fe817a23251b', 'IFE'], 
    ['09a53a9f-796a-49e3-8135-9c382153f921', 'Tyler Childers'],
    ['f2ca4ebe-e6fd-4447-b12e-600f89565910', 'Lara Bello'],
    ['c7bb4170-14a3-4723-a10d-f0a537135376', 'Masta Ace'],
    ['36179af9-a184-4fc2-a009-ee2ce7eaac06', "I'm With Her"], 
    ['0437a76f-f65c-4835-b453-b48d01017071', 'Jenny and the Mexicats'],
    ['d3154309-5cf3-474c-a2c1-be61696ffad6', 'Vasen'],
    ['dc5b9dac-ef39-43ee-bab5-ceaccbd7c3c9','Cornelius'], 
    ['f6b88646-4faa-408c-8942-1636a1b82b18', 'Raul Midon'],
    ['8a181927-79f8-45e7-ba02-65fe810838b3', 'John Prine'],
    ['0cb70805-da14-4d22-a8a7-04e31d4e7ef0', 'Kuinka'],
    ['3d95c66d-227c-4347-bafe-140d201f2fb1', 'Alex Clare'],
    ['831befd9-bc3e-45cb-b0ea-8b0b1db5376a', 'Anna Meredith'],
    ['1f3e4886-9718-424b-80ba-93163613e6ce', 'August Greene'],
    ['529a7c5a-47e5-4005-a0f8-f1f3966345f7', 'Betsayda Machado and Parranda El Clavo'],
    ['f840b8cb-2825-4467-ac66-1a4f6ba853ab', 'Nick Hakim'],
    ['96520d56-f378-4631-9c70-3225712b7fb7', 'Marlon Williams'],
    ['ae0ddaec-5b5b-42ee-8362-7d27c0bf4975', 'The Crossrhodes'],
    ['7d09e3fb-24dd-4bda-8fa1-0fbff8b9d32f', 'Ibeyi'],
    ['761f1a2a-6527-4d49-b413-d5d2ba1646cb', 'Vicente Garcia'],
    ['17cce023-1342-4fe5-b03a-4055a6bf3136', 'Alice Smith'],
    ['94827c60-7d14-4ff3-9823-c547ea91de14', 'Jamila Woods'],
    ['ad5e7162-5b8f-40bb-b5a6-308b4abf20e5', 'Barbara Hannigan'], 
    ['85378e50-7a02-4755-b879-1b1b11b7461d', 'George Clinton & The P-Funk All Stars'],
    ['52d2ded2-d104-4748-9b70-27c6140841fd', 'St. Vincent'], 
    ['569ed132-3234-4b60-ac4f-dd4159e67864', 'Artists From the "Take Me to the River" Tour'],
    ['9d7ef404-df36-49a6-a68b-20cd03763300', 'Hanson Holiday Tiny Desk Concert'], 
    ['a1f4958b-05b5-46df-89d9-a1f79623434d', 'This is the Kit'], 
    ['054f0844-a27e-4735-925c-32ed882a33a4', 'Cigarettes After Sex'],
    ['20b3f912-f233-4c77-836c-fdb98ab4a19f', 'Courtney Barnett and Kurt Vile'],
    ['69715b79-a733-4bc1-93c7-8e56f11c235a', 'Walter Martin'],
    ['67bef9ae-9dbf-48d9-911b-3676922565fe', 'Moses Sumney'], 
    ['8aa3ed83-ac72-4d61-9610-f56aaa6742e5', 'Phoebe Bridgers'],
    ['4660ec96-957c-46ad-9bb8-f29cb21d669f', 'Ledisi'], 
    ['2e6e653c-e018-4c5e-9d53-467af0c7a651', 'David Greilsammer'], 
    ['4f5fd52c-a046-4966-90f3-8cb3f3f2a549', 'Billy Corgan'],
    ['ef79e0a3-4e00-42da-8047-31928b117b54', 'Now, Now'], 
    ['2349b2d2-c462-4fb2-a266-900e0f6fba5e', 'Nate Smith + KINFOLK'],
    ['96ee6975-b07f-40d5-b88b-a0de6c1b99a5', 'Gracie and Rachel'], 
    ['b128b11d-ecbe-48b8-9cee-6bd8ea9bd035', 'The Roots feat. Bilal'], 
    ['8abbb206-f2a9-4b55-bf6a-a83339f1d831', 'Shabazz Palaces'],
    ['c25ee550-6861-4ca5-b8a2-194298e86deb', 'Randy Newman'],
    ['efdc46e4-4815-4549-b57b-d9b71a85d4c4', 'Landlady'], 
    ['d242c687-1c0b-40fd-b33a-1445d5d3f82f', 'Paramore'], 
    ['7145665c-6c06-4661-8c34-de0b719081b3', 'Dawg Yawp'], 
    ['8351398a-f628-4187-926e-1b4806d5a498', 'Chronixx'],
    ['932e39ec-6290-49cc-96c2-63c01e8b1d98', 'Steve Martin And The Steep Canyon Rangers'], 
    ['cc641797-6f86-42db-8991-cec7b507b9ee', 'Ssingssing'],
    ['1f89d4d7-9ce0-4ba1-9bc4-cea4e57432aa', 'L.A. Salami'],
    ['23afa374-99bc-4170-a5ba-0bbd545fdbfd', 'Frances Cone'],
    ['01f4ad51-dba0-4c0b-b7ae-e9050f1b1760', 'ALA.NI'],
    ['f3d4f197-6e19-4b5b-ac7f-854fbd8567d8', 'Albin Lee Meldau'],
    ['26a4b6b4-a59c-475a-a9ec-b6680143611a', 'Rare Essence'], 
    ['6e85bda7-32d3-42bb-ba76-a43bcec47524', 'Tuxedo'],
    ['9295aad2-e13f-414a-84bc-bfec327a765e', 'Fragile Rock'],
    ['42c2b54b-f548-48b7-a647-eac88b0eea83', 'Jay Som'],
    ['2369c535-2764-427d-8be8-70af83bb6ff1', 'Chance The Rapper'], 
    ['466c2708-fbc2-452d-bd06-fb8ed65f7411', 'Helado Negro'], 
    ['ff6a5615-43d9-4495-861e-d96ce5adbb47', 'Ravi Coltrane Quartet'],
    ['581fc513-4ad7-417b-9c9f-9b46b8e09831', 'Holly Macve'],
    ['2c9152c1-8572-4c6e-9e86-0690499fe6cc', 'Perfume Genius'], 
    ['a49b3067-0c60-4792-8e0b-68d77522b087', 'Violents & Monica Marten'],
    ['389b2cb9-00f3-479d-a7c7-8d32693aa1c3', 'Nick Grant'],
    ['27c4e9fc-0d21-458c-9ade-758031c2913a', 'Julia Jacklin'], 
    ['e91aa7fe-e6b7-4a54-beba-abfea83c29b5', 'Troker'],
    ['eb79dd76-3d1e-43b2-bf82-115d2ca6179b', 'Tim Darcy'], 
    ['1427864b-6a9a-4aee-a149-b862d071afaf', 'Danilo Brito'], 
    ['e42e5b30-1022-4484-a7a8-5275f4a6bc6c', 'Peter Silberman'],
    ['165cc1e3-7bdf-4ee4-a1a8-d0153d3d3fb9', 'Avery*Sunshine'],
    ['7f1b5b83-75c2-4d97-82a4-6c377e74012b', 'Antonio Lizana'],
    ['d28ed53a-68ac-47b6-b9a1-87d496b3269e', 'alt-J'],
    ['070f4bc9-4872-411a-a17b-95f218706dd9', 'Chicano Batman'],
    ['74a00599-af03-462f-a62d-6cfc8e4a8c72', 'Ljova and the Kontraband'],
    ['5c1a464b-4540-4bcf-8fe3-2622ec28e0a2', 'Sinkane'], 
    ['882a76b9-dbfa-4b2d-97fc-fbe5f6cc3e5f', 'Tash Sultana'],
    ['6efb0fbf-250b-40ee-a31d-9bba9f5c8208', 'Noname'],
    ['3eed3b01-e398-44ef-a998-f2f86282322a', 'Overcoats'],
    ['45b3e707-8c25-43ec-9f14-78bb270ed645', 'Red Baraat'],
    ['8579a11d-8444-41da-b8ef-2499aa6c3dd8', 'Tank And The Bangas'], 
    ['d7c9dc95-2655-4f0a-9cd6-ad65bfc1eef9', 'Little Simz'], 
    ['9419b5e5-03cd-4b2c-b9fb-d1b8af925985', 'Run The Jewels'], 
    ['ace4f1e9-5891-49db-b2b7-8c630cf23aa5', 'Gallant'],
    ['3c237cc4-636f-48fd-b370-6fadff2355b9', 'Miramar'], 
    ['7c7741eb-f81c-4b31-be26-d03e6b87283b', 'BADBADNOTGOOD'],
    ['77e0be24-f49e-437f-aa9c-45bfa41b70b7', 'Brent Cobb'],
    ['853bfe06-28f7-447a-8af1-df516c82bf69', 'Lila Downs'],
    ['446447e5-b17a-48d0-88b0-a41017a40e3e', 'Donny McCaslin'],
    ['f2a24501-51a1-4320-bc64-2b71c94c1ab8', 'Declan McKenna'],
    ['586e38aa-8ce9-415d-89f2-9f3af7f52a6e', 'The Oh Hellos: Holiday Tiny Desk Concert'], 
    ['6786e146-add6-4d6d-a4a8-192739bd0e6a', 'Derek Gripper'], 
    ['b64811cf-6a88-4203-b22a-387efc70ea9a', 'Ro James'],
    ['fcd2ad97-ef71-4e8d-8238-08016cc47e4a', 'Margo Price'],
    ['99de8518-bc1a-4246-9e75-9bfef511bb55', 'Attacca Quartet'],
    ['7570d218-198d-490c-bb81-4d1a5173554d', 'Adam Torres'],
    ['6bc20714-2c63-499f-9af6-1787b8e00f47', 'Ta-ku & Wafia'],
    ['8daaffec-922e-4fd3-ac04-984adffc7ac9', 'The Westerlies'], 
    ['99e2e0bc-9329-48d6-92f0-91600431e24a', 'Blind Pilot'], 
    ['cab1223d-9d71-4d21-9583-e481782da11f', 'Billy Bragg & Joe Henry'],
    ['130188af-f4be-44eb-9fe9-871dedc48ac8', 'RDGLDGRN'], 
    ['4c533362-fe20-4ec3-a1f3-73276a760324', 'Haley Bonar'], 
    ['6d457215-63a4-4fcc-aabd-ef87b8e6cda8', 'Common At The White House'],
    ['c3c9bd05-5cac-4e4c-818a-8cdb217c5719', 'Joshua Bell & Jeremy Denk'],
    ['57fcd843-99b0-4f00-b5a9-7661216baae3', 'Blue Man Group'], 
    ['837f724d-7d4d-4f1f-9586-14ed71bfe8e7', 'The Secret Sisters'], 
    ['df336c38-4524-4b0d-8370-c7a24017a441', 'Nina Diaz'],
    ['ae9b75e1-2a4a-4f9a-a5b8-9571ccda43fc', 'Margaret Glaspy'],
    ['f5c6172c-5a65-4739-87e3-c1dc49e34336', 'Rene Marie'],
    ['a29bc63c-e05d-479e-ae53-f5e64d9b095e', 'Xenia Rubinos'],
    ['d6e5d657-1b52-4489-a9ad-06ec922f33eb', 'John Congleton And The Nighty Nite'], 
    ['2a3a183b-1f18-41ee-8b70-e1f646a3802a', 'Gregory Porter'],
    ['a17d791f-345f-4603-b1d2-2dbbf07fc773', 'Chris Forsyth & The Solar Motel Band'],
    ['253713e4-bd13-4eac-8437-b082077ee84f', 'Jane Bunnett and Maqueque'],
    ['16c20188-f8f8-428f-bef9-12a2325a3082', 'Valley Queen'], 
    ['3ed3b8b2-a48b-4612-9c73-d678b29b7d2b', 'Los Hacheros'],
    ['57fc8717-0743-4ef1-89e6-a02a13281dd4', 'Adia Victoria'],
    ['10d0ab59-5e32-463e-8ed1-f64cd61b7ba5', 'Wyclef Jean'],
    ['287a6ae2-9618-48af-b330-ff16d3c32caf', 'Erykah Badu'], 
    ['9bdd37f6-e31e-452a-b918-43c01e1e6c31', 'Esme Patterson'], 
    ['11b92baa-43f2-4aa3-a24e-1027a8948878', 'Anthony Roth Costanzo'], 
    ['9223bce6-8540-4ec2-82af-3b232f486135', 'Maggie Rogers'], 
    ['1f60e998-edc7-4a40-a8e7-1ceeb2dbe857', 'Khalid'], 
    ['b062ba95-1910-4312-bb27-8ae1e42a8fd3', 'Delicate Steve'], 
    ['881d3907-a4bb-4f4c-9ad7-90c65fce7aeb', 'Agnes Obel'], 
    ['f9743dcf-6354-492c-b4ae-0dd13a93299f', 'D.R.A.M.'], 
    ['4b21e890-27a1-4eef-abc7-a0c5b6b9305d', 'Jason Isbell'],
    ['ed73c51d-f1df-48ff-b636-ce18f2c4e306', 'DJ Premier & The Badder Band'],
    ['6cd4f9c5-431f-40a6-ae75-580ff40af024', 'Blood Orange'],
    ['5055526b-65fb-481c-bf0b-adb5bcad7b8f', 'Ninet'],
    ['4f3cb742-de5e-4efd-9c75-cccaa67e5116', 'Lee Ann Womack'],
    ['a6576fef-1b73-4217-988d-0a748a46f2ae', 'Grace VanderWaal'],
    ['0a09868c-735c-4113-bcd1-fa2da7bf6d07', 'Logan Richardson'],
    ['ad15fa01-d9da-4873-81fe-ff22be7f5646', 'Alfredo Rodriguez'],
    ['9da5b05c-8257-4ed7-89f5-97289c20918c', 'Kurt Vile'],
    ['4cfd8e3a-7d84-45ff-bbc7-46936801b00f', 'Corinne Bailey Rae'],
    ['41639bb6-019a-41c5-b382-e64c8e46f744', 'DAWN'],
    ['142d3c88-6e3e-4007-8fdc-bd7d4bd3de3b', 'Jorja Smith'], 
    ['5a83291a-0007-441b-b960-cad839e7424d', 'Superorganism'],
    ['3cb8d2ac-99d3-48e9-b367-29f9d550275b', 'King Krule'], 
    ['75336437-5cef-44fe-9dd1-89fca96458b2', 'Penguin Cafe'], 
    ['b776fae0-1b52-4235-af09-8085564e378e', 'The Lemon Twigs'],
    ['750640a8-7434-4af6-aea2-c3804e4ad810', 'John Moreland'],
    ['a346a4ad-45a9-4813-855a-5ac302b9a85a', 'John Paul White'],
    ['6012dbcd-8f74-43dc-94a5-4a19f3d337c1', 'Better Oblivion Community Center'],
    ['ae1ba7f8-8c6f-4bb6-b663-da6020c37226', 'Georgia Anne Muldrow'],
    ['9c89dc30-9333-4a8d-88ac-2f0c2717c7ee', 'Weezer'], 
    ['bf93a173-f890-4f94-8cc2-cc854e5f3e54', 'Roy Ayers'],
    ['384f980e-6564-47d8-b4fd-5dd14e8c3c66', 'Lo Moon'], 
    ['fb2d9b59-962b-4b53-bae9-a39d7d0606a9', 'Tyler, The Creator'],
    ['26a6d64f-c8fa-41b9-90f6-2d19617de4f7', 'Thundercat'],
    ['ed980d7f-d8da-4350-9f8a-4baed5919e4f', 'Jim James'], 
    ['0ef34a72-503d-44c5-afb5-31b4615e80bb', 'Buddy'],
    ['9a420b49-799f-4ee8-939e-2f208e79fa52', 'Kevin Morby'],
    ['f7620b47-79e1-4362-ba51-6a2959cd6975', 'Juanes & Mon Laferte'], 
    ['d139260b-bc5a-440e-9551-b9b7986698f3','Camp Cope'], 
    ['d969562e-d6df-4bab-86cf-fa7c821f0cdc', 'Dee Dee Bridgewater'], 
    ['e8ade6e0-42d4-4ab2-98d2-1496d4e9f094', 'Julien Baker'], 
    ['02e42bb1-4787-4cb1-86aa-de075ae551ea', 'William Bell'],
    ['e75c4498-a32f-4453-b3b2-2f38ae81e671', 'Charles Lloyd & Jason Moran'], 
    ['f9beb4ae-90e0-4818-9b76-be16da881956', 'Big K.R.I.T.'], 
    ['6a896434-e6a0-4b81-bcb3-25d1358595ae', 'Cecile McLorin Salvant'],
    ['32081d4c-2e2b-4dbf-8d0d-3eefd40bc200', 'The Jayhawks'],
    ['2aa87ac2-8732-41bb-af20-ff247557651d', 'Pinegrove'],
    ['2c72df91-cd20-4099-98c4-d904062d8a2e', 'Jorge Drexler'],
    ['3506d1ec-5dbc-40c0-beab-2e6146c54788', 'Kaia Kater'],
    ['97838b48-14d1-4302-bae8-bf9887bcd049', 'Chromeo'], 
    ['bec781c5-3fe5-4871-8dff-9b7c0df35775', 'Sampha'], 
    ['cd073b75-d24f-4fbb-ac92-460700f1a378', 'Olafor Arnalds'],
    ['ff5095de-a2a1-4251-a970-8ab6450cc088', 'The Del McCoury Band'],
    ['cdb97c04-98c7-4945-b42e-876a8a65ee66', 'Hurray For The Riff Raff'],
    ['381e3615-883d-4400-a52e-18d0a4ecf811', 'Dirty Dozen Brass Band'],
    ['e2511655-2c25-4430-b793-82190afd42e6', 'Diet Cig'], 
    ['fd0ff2b1-d9d2-43ab-81de-8cae7d4f4fa8', 'Saul Williams'],
    ['57b364e8-1083-456c-821f-7d581df60a05', 'Tower Of Power'],
    ['389948fd-9357-4592-9af9-54bd667733f0', 'The Mynabirds'],
    ['5dedaa2b-9302-4415-9e44-12a890c87c81', 'Anderson .Paak & The Free Nationals'],
    ['b27e8631-547c-4594-80c6-9a1d77ad64fb', 'Yo-Yo Ma'], 
    ['07d42e14-f65c-4677-8f68-5cd1d1454a29', 'Japanese Breakfast'],
    ['8d96d33a-5964-4184-8667-fc00b82a9b99', 'Courtney Marie Andrews'],
    ['8d7ea534-6aed-40ef-ab1d-4675dd92271b', 'Mac Miller'],
    ['0db5ef21-8caf-4815-94b7-cc0248345b28', 'AminA'],
    ['add0a3f5-63bc-4625-abd8-4bdc88adac41', 'Aimee Mann'], 
    ['04c9efec-7503-4975-9957-e56a0478ab83', 'Lucy Dacus'],
    ['c2f41f93-ece5-4239-b280-d9c594eae417', 'Joseph'], 
    ['61ef5f4b-48ce-41eb-92fd-f365016e07ee', 'Alejandro Escovedo'], 
    ['b53b59d3-ac37-439a-b487-4f4a5d7b49e6', 'Big Boi'],
    ['dbd5886e-593b-4a04-b2fb-c94cad8d3be5', 'Tigers Jaw'], 
    ['3b08576a-a357-4e01-a29e-3b7393090dda', 'Pedro The Lion'], 
    ['06a69108-53ed-4334-9937-979d8b0f41de', 'Ted Leo'], 
    ['7b1ede94-6a90-450c-a164-bed7c1cd9750', 'Wu-Tang Clan'], 
    ['cc42f8cb-4d49-4551-9ec2-61bfe1e1b841', 'Haley Heynderickx'],
    ['29f8dc7c-1187-4d01-9a33-a562870984a2', 'Alsarah & The Nubatones'],
    ['cc2ca193-c958-4a58-a137-ad89f616e870', 'Stella Donnelly'], 
    ['74daf07e-4ca6-4b14-8cc8-107d2f7276e3', 'Eddie Palmieri'],
    ['ffe64431-3092-443f-b0ad-82130dad42b7', 'Daniel Caesar'],
    ['59b4cdf1-f2a7-4a47-b627-c8f890eafb82', 'Rhye'], 
    ['f5528ec9-91bb-42e4-9f2d-60e4fe9af8f0', 'The Weather Station'],
    ['1b8c7085-22ef-4068-b86b-97f956efdb21', 'Hanson'], 
    ['5a5bb055-9b72-40c6-b688-9db073da7536', 'Benjamin Booker'], 
    ['a4695d1c-e9ae-4988-bf12-06a48ab4fcf7', 'GoldLink'], 
    ['8ef6833b-d951-49a8-91bd-d2108db48d68', 'Trouble Funk'], 
    ['cf6d202b-9607-48f2-b44b-76bb3f072ca3', 'Jidenna'],
    ['ab23c5b9-8835-4c87-b880-644032a92e1b', 'Rakim'], 
    ['82426d3c-3fe0-4b48-bef9-9b6efeebdb8a', 'Vagabon']
]}

artistTable = createArtistConcertTrackerLayer(workspace,artistLookupTableName)
addFields(artistTable, fields)
addDomains(workspace, domains)
addRatings(workspace)
addDomainValues(workspace,artistDomains)
assignDomainToField(artistTable, "artist", 'artists') 
assignDomainToField(artistTable, "rating", 'rating') 

