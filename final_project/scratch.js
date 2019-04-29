   var find = new FindTask(nprMapService);
                        var params = new FindParameters();
                        params.layerIds = [0];
                        params.searchFields = ["title","description", "pubDate", "guid_", "imgLink", "actURL", "NEAR_DIST"];
                        find.execute(params, createArtistTOC);
                        console.log('Executed Query for Artist Ref info')
                    