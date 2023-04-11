function svuota()
{
  if (confirm("Eliminare tutti gli articoli dal carrello?")) 
  {
    location.href='/svuotaCarrello'
  }
}

function acq_art()
{
  if (confirm("Procedere con l'acquisto?")) 
  {
    location.href='/acquista'
  } 
}