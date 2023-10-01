workspace "Name" "Description" {

    model {
        mrc = softwareSystem "MagentaRapidsCore" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        mrf = softwareSystem "MagentaRapidsFrontend" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        mrcl = softwareSystem "MagentaRapidsClient" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        emc = softwareSystem "External MIDI Controler" {
            # typical example: KORG Keyboard, something with MIDI out
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
            }
        }
        emb = softwareSystem "External MIDI Backend" {
            # typical example: DAW, something with MIDI in
            perspectives {
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        p = person "User" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        
        # Submission Process
        p -> emc "Trigger" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
            }
        }
        emc -> mrcl "Sends raw MIDI" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
            }
        }
        mrcl -> mrf "Sends buffered MIDI" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
            }
        }
        mrf -> mrc "Store and process buffered MIDI" {
            perspectives {
                "Submission Process" "Standard process for getting MIDI from a user into a Magenta Rapids environment"
            }
        }
        
        # Client-Frontend Subscription Process
        mrcl -> mrf "Subscribe to channel"
        # Client and external controllers/backends communicate locally over MIDI ports
        
        # Broadcast Process
        mrc -> mrf "Send buffered, processed MIDI" {
            perspectives {
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        mrf -> mrcl "Broadcast buffered MIDI" {
            perspectives {
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        mrcl -> emb "Send raw MIDI" {
            perspectives {
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        emb -> p "Render MIDI" {
            perspectives {
                "Broadcast Process" "Standard process for getting MIDI from a Magenta Rapids environment out to users"
            }
        }
        
    }
    
    views {
        systemLandscape mrc {
            include *
        }
    }
}